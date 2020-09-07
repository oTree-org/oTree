#!/usr/bin/env python
# -*- coding: utf-8 -*-

from otree.common_internal import get_models_module
from otree_save_the_change.mixins import SaveTheChange
from otree.db import models
from otree.models.fieldchecks import ensure_field

ATTRIBUTE_ERROR_MESSAGE = '''
Player object has no attribute '{}'. If it is a model field or method,
it must be declared on the Player class in models.py.
'''.replace('\n', ' ')


class BasePlayer(SaveTheChange, models.Model):
    """
    Base class for all players.
    """

    class Meta:
        abstract = True
        index_together = ['participant', 'round_number']
        ordering = ['pk']

    id_in_group = models.PositiveIntegerField(
        null=True,
        db_index=True,
        doc=("Index starting from 1. In multiplayer games, "
             "indicates whether this is player 1, player 2, etc.")
    )

    payoff = models.CurrencyField(
        null=True,
        doc="""The payoff the player made in this subsession""",
    )

    participant = models.ForeignKey(
        'otree.Participant', related_name='%(app_label)s_%(class)s'
    )

    session = models.ForeignKey(
        'otree.Session', related_name='%(app_label)s_%(class)s'
    )

    round_number = models.PositiveIntegerField(db_index=True)

    def __getattribute__(self, name):
        try:
            return super(BasePlayer, self).__getattribute__(name)
        except AttributeError:
            # this will result in "during handling of the above exception...'
            # once we drop Python <3.3, we can raise from None
            # for now, it's not that bad, just the almost same error printed
            # twice
            raise AttributeError(ATTRIBUTE_ERROR_MESSAGE.format(name))

    # it's _name instead of name because people might define
    # their own name field
    def _name(self):
        return self.participant.__unicode__()

    @property
    def id_in_subsession(self):
        return self.participant.id_in_session

    def __repr__(self):
        id_in_subsession = self.id_in_subsession
        if id_in_subsession < 10:
            # 2 spaces so that it lines up if printing a matrix
            fmt_string = '<Player  {}>'
        else:
            fmt_string = '<Player {}>'
        return fmt_string.format(id_in_subsession)

    def role(self):
        # you can make this depend of self.id_in_group
        return ''

    def in_round(self, round_number):
        return type(self).objects.get(
            participant=self.participant, round_number=round_number
        )

    def in_rounds(self, first, last):
        qs = type(self).objects.filter(
            participant=self.participant, round_number__range=(first, last),
        ).order_by('round_number')

        return list(qs)

    def in_previous_rounds(self):
        return self.in_rounds(1, self.round_number - 1)

    def in_all_rounds(self):
        return self.in_previous_rounds() + [self]

    def get_others_in_group(self):
        return [p for p in self.group.get_players() if p != self]

    def get_others_in_subsession(self):
        return [p for p in self.subsession.get_players() if p != self]

    def __unicode__(self):
        return self._name()

    def _GroupClass(self):
        return self._meta.get_field('group').rel.to

    @property
    def _Constants(self):
        return get_models_module(self._meta.app_config.name).Constants

    @classmethod
    def _ensure_required_fields(cls):
        """
        Every ``Player`` model requires a foreign key to the ``Subsession`` and
        ``Group`` model of the same app.
        """
        subsession_model = '{app_label}.Subsession'.format(
            app_label=cls._meta.app_label)
        subsession_field = models.ForeignKey(subsession_model)
        ensure_field(cls, 'subsession', subsession_field)

        group_model = '{app_label}.Group'.format(
            app_label=cls._meta.app_label)
        group_field = models.ForeignKey(group_model, null=True)
        ensure_field(cls, 'group', group_field)
