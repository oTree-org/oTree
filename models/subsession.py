from django.db.models import Prefetch
from otree.db import models
from otree.common_internal import (
    get_models_module, in_round, in_rounds)
from otree import matching
import copy
from otree.common_internal import has_group_by_arrival_time, add_field_tracker


class GroupMatrixError(ValueError):
    pass


class RoundMismatchError(GroupMatrixError):
    pass

class BaseSubsession(models.Model):
    """Base class for all Subsessions.
    """

    class Meta:
        abstract = True
        ordering = ['pk']
        index_together = ['session', 'round_number']

    session = models.ForeignKey(
        'otree.Session', related_name='%(app_label)s_%(class)s', null=True,
        on_delete=models.CASCADE,
    )

    round_number = models.PositiveIntegerField(
        db_index=True,
        doc='''If this subsession is repeated (i.e. has multiple rounds), this
        field stores the position of this subsession, among subsessions
        in the same app.
        '''
    )

    def in_round(self, round_number):
        return in_round(type(self), round_number,
            session=self.session,
        )

    def in_rounds(self, first, last):
        return in_rounds(type(self), first, last, session=self.session)

    def in_previous_rounds(self):
        return self.in_rounds(1, self.round_number-1)

    def in_all_rounds(self):
        return self.in_previous_rounds() + [self]

    def __unicode__(self):
        return str(self.pk)

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
            raise GroupMatrixError(
                'Group matrix must be a list of lists.'
            ) from None
        try:
            matrix_pks = sorted(p.pk for p in players_flat)
        except AttributeError:
            # if integers, it's OK
            if isinstance(players_flat[0], int):
                # deep copy so that we don't modify the input arg
                matrix = copy.deepcopy(matrix)
                players_flat = sorted(players_flat)
                players_from_db = self.get_players()
                if players_flat == list(range(1, len(players_from_db) + 1)):
                    for i, row in enumerate(matrix):
                        for j, val in enumerate(row):
                            matrix[i][j] = players_from_db[val - 1]
                else:
                    raise GroupMatrixError(
                        'If you pass a matrix of integers to this function, '
                        'It must contain all integers from 1 to '
                        'the number of players in the subsession.'
                    ) from None
            else:
                raise GroupMatrixError(
                    'The elements of the group matrix '
                    'must either be Player objects, or integers.'
                ) from None
        else:
            existing_pks = list(
                self.player_set.values_list(
                    'pk', flat=True
                ).order_by('pk'))
            if matrix_pks != existing_pks:
                wrong_round_numbers = [
                    p.round_number for p in players_flat
                    if p.round_number != self.round_number]
                if wrong_round_numbers:
                    raise GroupMatrixError(
                        'You are setting the groups for round {}, '
                        'but the matrix contains players from round {}.'.format(
                            self.round_number,
                            wrong_round_numbers[0]
                        )
                    )
                raise GroupMatrixError(
                    'The group matrix must contain each player '
                    'in the subsession exactly once.'
                )

        # Before deleting groups, Need to set the foreignkeys to None
        # 2016-11-8: does this need to be in a transaction?
        # because what if a player refreshes their page while this is going
        # on?
        self.player_set.update(group=None)
        self.group_set.all().delete()

        GroupClass = self._GroupClass()
        for i, row in enumerate(matrix, start=1):
            group = GroupClass.objects.create(
                subsession=self, id_in_subsession=i,
                session=self.session, round_number=self.round_number)

            group.set_players(row)

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

    def new_group_like_round(self, round_number):
        '''test this, could work'''
        matrix = self.in_round(round_number).get_group_matrix()
        for row in matrix:
            for col in row:
                matrix[row][col] = matrix[row][col].id_in_subsession
        self.set_group_matrix(matrix)

    '''
    def group_like_round(self, round_number):
        PlayerClass = self._PlayerClass()
        last_round_info = PlayerClass.objects.filter(
            session_id=self.session_id,
            round_number=round_number
        ).values(
            'id_in_group', 'participant_id', 'group__id_in_subsession'
        ).order_by('group__id_in_subsession', 'id_in_group')

        player_lookups = {p.participant_id: p for p in self.get_players()}

        self.player_set.update(group=None)
        self.group_set.all().delete()

        # UNFINISHED
        GroupClass = self._GroupClass()
        for i, row in enumerate(matrix, start=1):
            group = GroupClass.objects.create(
                subsession=self, id_in_subsession=i,
                session=self.session, round_number=self.round_number)

            group.set_players(row)
    '''


    def set_groups(self, matrix):
        '''renamed this to set_group_matrix, but keeping in for compat'''
        return self.set_group_matrix(matrix)

    @property
    def _Constants(self):
        return get_models_module(self._meta.app_config.name).Constants

    def _GroupClass(self):
        return models.get_model(self._meta.app_config.label, 'Group')

    def _PlayerClass(self):
        return models.get_model(self._meta.app_config.label, 'Player')

    @classmethod
    def _has_group_by_arrival_time(cls):
        return has_group_by_arrival_time(cls._meta.app_config.name)


    def group_randomly(self, *, fixed_id_in_group=False):
        group_matrix = self.get_group_matrix()
        group_matrix = matching.randomly(
            group_matrix,
            fixed_id_in_group)
        self.set_group_matrix(group_matrix)

    def _group_by_rank(self, ranked_list):
        # FIXME: delete this
        group_matrix = matching.by_rank(
            ranked_list,
            self._Constants.players_per_group
        )
        self.set_group_matrix(group_matrix)

    def before_session_starts(self):
        '''Deprecated and renamed to creating_session'''
        pass

    def creating_session(self):
        pass

    def vars_for_admin_report(self):
        return {}

    @classmethod
    def _ensure_required_fields(cls):
        add_field_tracker(cls)