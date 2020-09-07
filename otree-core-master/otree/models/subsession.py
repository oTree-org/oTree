#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division

import six
from django.db.models import Prefetch
from otree_save_the_change.mixins import SaveTheChange
from otree.db import models
from otree.common_internal import get_models_module
from otree import matching
import copy

ATTRIBUTE_ERROR_MESSAGE = '''
Subsession object has no attribute '{}'. If it is a model field or method,
it must be declared on the Subsession class in models.py.
'''.replace('\n', '')


class BaseSubsession(SaveTheChange, models.Model):
    """Base class for all Subsessions.
    """

    class Meta:
        abstract = True
        ordering = ['pk']
        index_together = ['session', 'round_number']

    session = models.ForeignKey(
        'otree.Session', related_name='%(app_label)s_%(class)s', null=True)

    round_number = models.PositiveIntegerField(
        db_index=True,
        doc='''If this subsession is repeated (i.e. has multiple rounds), this
        field stores the position (index) of this subsession, among subsessions
        in the same app.

        For example, if a session consists of the subsessions:

            [app1, app2, app1, app1, app3]

        Then the round numbers of these subsessions would be:

            [1, 1, 2, 3, 1]

        '''
    )

    def __getattribute__(self, name):
        try:
            return super(BaseSubsession, self).__getattribute__(name)
        except AttributeError:
            # this will result in "during handling of the above exception...'
            # once we drop Python <3.3, we can raise from None
            # for now, it's not that bad, just the almost same error printed
            # twice
            raise AttributeError(ATTRIBUTE_ERROR_MESSAGE.format(name))

    def in_rounds(self, first, last):
        qs = type(self).objects.filter(
            session=self.session,
            round_number__range=(first, last),
        ).order_by('round_number')

        return list(qs)

    def in_previous_rounds(self):
        return self.in_rounds(1, self.round_number-1)

    def in_all_rounds(self):
        return self.in_previous_rounds() + [self]

    def name(self):
        return str(self.pk)

    def __unicode__(self):
        return self.name()

    @property
    def app_name(self):
        return self._meta.app_config.name

    def in_round(self, round_number):
        return type(self).objects.get(
            session=self.session,
            round_number=round_number
        )

    def _get_players_per_group_list(self):
        """get a list whose elements are the number of players in each group

        Example: a group of 30 players

        # everyone is in the same group
        [30]

        # 5 groups of 6
        [6, 6, 6, 6, 6,]

        # 2 groups of 5 players, 2 groups of 10 players
        [5, 10, 5, 10] # (you can do this with players_per_group = [5, 10]

        """

        ppg = self._Constants.players_per_group
        subsession_size = self.player_set.count()
        if ppg is None:
            return [subsession_size]

        # if groups have variable sizes, you can put it in a list
        if isinstance(ppg, (list, tuple)):
            assert all(n > 1 for n in ppg)
            group_cycle = ppg
        else:
            assert isinstance(ppg, six.integer_types) and ppg > 1
            group_cycle = [ppg]

        num_group_cycles = subsession_size // sum(group_cycle)
        return group_cycle * num_group_cycles

    def get_groups(self):
        return list(self.group_set.order_by('id_in_subsession'))

    def get_players(self):
        return list(self.player_set.order_by('pk'))

    def get_group_matrix(self):
        players_prefetch = Prefetch(
            'player_set',
            queryset=self._PlayerClass().objects.order_by('id_in_group'),
            to_attr='_ordered_players')
        return [group._ordered_players
                for group in self.group_set.order_by('id_in_subsession')
                                 .prefetch_related(players_prefetch)]

    def set_group_matrix(self, matrix):
        """
        warning: this deletes the groups and any data stored on them
        TODO: we should indicate this in docs
        """

        try:
            players_flat = [p for g in matrix for p in g]
        except TypeError:
            raise TypeError(
                'Group matrix must be a list of lists.'
            )
        try:
            matrix_pks = sorted(p.pk for p in players_flat)
        except AttributeError:
            # if integers, it's OK
            if isinstance(players_flat[0], int):
                # deep copy so that we don't modify the input arg
                matrix = copy.deepcopy(matrix)
                players_flat = sorted(players_flat)
                if players_flat == list(range(1, len(players_flat) + 1)):
                    players = self.get_players()
                    for i, row in enumerate(matrix):
                        for j, val in enumerate(row):
                            matrix[i][j] = players[val - 1]
                else:
                    raise ValueError(
                        'If you pass a matrix of integers to this function, '
                        'It must contain all integers from 1 to '
                        'the number of players in the subsession.'
                    )
            else:
                raise TypeError(
                    'The elements of the group matrix '
                    'must either be Player objects, or integers.'
                )

        else:
            existing_pks = list(
                self.player_set.values_list(
                    'pk', flat=True
                ).order_by('pk'))
            if matrix_pks != existing_pks:
                raise ValueError(
                    'The group matrix must contain each player '
                    'in the subsession exactly once.'
                )

        # Before deleting groups, Need to set the foreignkeys to None
        self.player_set.update(group=None)
        self.group_set.all().delete()

        GroupClass = self._GroupClass()
        for i, row in enumerate(matrix, start=1):
            group = GroupClass.objects.create(
                subsession=self, id_in_subsession=i,
                session=self.session, round_number=self.round_number)

            group.set_players(row)

    def set_groups(self, matrix):
        '''renamed this to set_group_matrix, but keeping in for compat'''
        return self.set_group_matrix(matrix)

    def check_group_integrity(self):
        ''' should be moved from here to a test case'''
        players = self.player_set.values_list('pk', flat=True)
        players_from_groups = self.player_set.filter(
            group__subsession=self).values_list('pk', flat=True)
        if not set(players) == set(players_from_groups):
            raise Exception('Group integrity check failed')

    @property
    def _Constants(self):
        return get_models_module(self._meta.app_config.name).Constants

    def _GroupClass(self):
        return models.get_model(self._meta.app_config.label, 'Group')

    def _PlayerClass(self):
        return models.get_model(self._meta.app_config.label, 'Player')

    def _first_round_group_matrix(self):
        players = list(self.get_players())

        groups = []
        first_player_index = 0

        for group_size in self._get_players_per_group_list():
            groups.append(
                players[first_player_index:first_player_index + group_size]
            )
            first_player_index += group_size
        return groups

    def _create_groups(self):
        if self.round_number == 1:
            group_matrix = self._first_round_group_matrix()
            self.set_group_matrix(group_matrix)
        else:
            self.group_like_round(1)

    def group_like_round(self, round_number):
        previous_round = self.in_round(round_number)
        group_matrix = [
            group._ordered_players
            for group in previous_round.group_set.order_by(
                'id_in_subsession'
            ).prefetch_related(
                Prefetch(
                    'player_set',
                    queryset=self._PlayerClass().objects.order_by(
                        'id_in_group'),
                    to_attr='_ordered_players'
                )
            )
        ]
        for i, group_list in enumerate(group_matrix):
            for j, player in enumerate(group_list):
                # for every entry (i,j) in the matrix, follow the pointer
                # to the same person in the next round
                group_matrix[i][j] = player.in_round(self.round_number)

        self.set_group_matrix(group_matrix)

    def group_randomly(self, fixed_id_in_group=False):
        group_matrix = self.get_group_matrix()
        group_matrix = matching.randomly(
            group_matrix,
            fixed_id_in_group)
        self.set_group_matrix(group_matrix)

    def group_by_rank(self, ranked_list):
        group_matrix = matching.by_rank(
            ranked_list,
            self._Constants.players_per_group
        )
        self.set_group_matrix(group_matrix)

    def before_session_starts(self):
        '''This gets called at the beginning of every subsession, before the
        first page is loaded.

        3rd party programmer can put any code here, e.g. to loop through
        players and assign treatment parameters.

        '''
        pass
