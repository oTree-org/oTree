#!/usr/bin/env python
# -*- coding: utf-8 -*-

from otree_save_the_change.mixins import SaveTheChange

from otree.db import models
from otree.common_internal import get_models_module
from otree.models.fieldchecks import ensure_field
import django.core.exceptions

ATTRIBUTE_ERROR_MESSAGE = '''
Group object has no attribute '{}'. If it is a model field or method,
it must be declared on the Group class in models.py.
'''.replace('\n', '')


class BaseGroup(SaveTheChange, models.Model):
    """Base class for all Groups.
    """

    class Meta:
        abstract = True
        index_together = ['session', 'id_in_subsession']
        ordering = ['pk']

    def __getattribute__(self, name):
        try:
            return super(BaseGroup, self).__getattribute__(name)
        except AttributeError:
            # this will result in "during handling of the above exception...'
            # once we drop Python <3.3, we can raise from None
            # for now, it's not that bad, just the almost same error printed
            # twice
            raise AttributeError(ATTRIBUTE_ERROR_MESSAGE.format(name))

    _is_missing_players = models.BooleanField(default=False, db_index=True)

    id_in_subsession = models.PositiveIntegerField(db_index=True)

    session = models.ForeignKey(
        'otree.Session', related_name='%(app_label)s_%(class)s'
    )

    round_number = models.PositiveIntegerField(db_index=True)

    def __unicode__(self):
        return str(self.pk)

    def get_players(self):
        return list(self.player_set.order_by('id_in_group'))

    def get_player_by_id(self, id_in_group):
        try:
            return self.player_set.get(id_in_group=id_in_group)
        except django.core.exceptions.ObjectDoesNotExist:
            raise ValueError(
                'No player with id_in_group {}'.format(id_in_group))

    def get_player_by_role(self, role):
        for p in self.get_players():
            if p.role() == role:
                return p
        raise ValueError('No player with role {}'.format(role))

    def set_players(self, players_list):
        for i, player in enumerate(players_list, start=1):
            player.group = self
            player.id_in_group = i
            player.save()

    def in_round(self, round_number):
        '''You should not use this method if
        you are rearranging groups between rounds.'''

        return type(self).objects.get(
            session=self.session,
            id_in_subsession=self.id_in_subsession,
            round_number=round_number,
        )

    def in_rounds(self, first, last):
        '''You should not use this method if
        you are rearranging groups between rounds.'''

        qs = type(self).objects.filter(
            session=self.session,
            id_in_subsession=self.id_in_subsession,
            round_number__range=(first, last),
        ).order_by('round_number')

        ret = list(qs)
        assert len(ret) == last-first+1
        return ret

    def in_previous_rounds(self):
        return self.in_rounds(1, self.round_number-1)

    def in_all_rounds(self):
        return self.in_previous_rounds() + [self]

    @property
    def _Constants(self):
        return get_models_module(self._meta.app_config.name).Constants

    @classmethod
    def _ensure_required_fields(cls):
        """
        Every ``Group`` model requires a foreign key to the ``Subsession``
        model of the same app.
        """
        subsession_model = '{app_label}.Subsession'.format(
            app_label=cls._meta.app_label)
        subsession_field = models.ForeignKey(subsession_model)
        ensure_field(cls, 'subsession', subsession_field)
