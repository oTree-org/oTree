#!/usr/bin/env python
# -*- coding: utf-8 -*-

from otree.common_internal import (
    add_field_tracker,
    get_models_module, in_round, in_rounds)

from otree.db import models
from otree.models.fieldchecks import ensure_field



class BasePlayer(models.Model):
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

    # don't modify this directly! Set player.payoff instead
    _payoff = models.CurrencyField(
        null=True,
        doc="""The payoff the player made in this subsession""",
        default=0
    )

    participant = models.ForeignKey(
        'otree.Participant', related_name='%(app_label)s_%(class)s',
        on_delete=models.CASCADE
    )

    session = models.ForeignKey(
        'otree.Session', related_name='%(app_label)s_%(class)s',
        on_delete=models.CASCADE
    )

    round_number = models.PositiveIntegerField(db_index=True)

    _gbat_arrived = models.BooleanField(default=False)
    _gbat_grouped = models.BooleanField(default=False)

    @property
    def payoff(self):
        return self._payoff

    @payoff.setter
    def payoff(self, value):
        if value is None:
            value = 0
        delta = value - self._payoff
        self._payoff += delta
        self.participant.payoff += delta
        # should save it because it may not be obvious that modifying
        # player.payoff also changes a field on a different model
        self.participant.save()

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
        return in_round(type(self), round_number, participant=self.participant)

    def in_rounds(self, first, last):
        return in_rounds(type(self), first, last, participant=self.participant)

    def in_previous_rounds(self):
        return self.in_rounds(1, self.round_number - 1)

    def in_all_rounds(self):
        '''i do it this way because it doesn't rely on idmap'''
        return self.in_previous_rounds() + [self]

    def get_others_in_group(self):
        return [p for p in self.group.get_players() if p != self]

    def get_others_in_subsession(self):
        return [p for p in self.subsession.get_players() if p != self]

    @classmethod
    def _ensure_required_fields(cls):
        """
        Every ``Player`` model requires a foreign key to the ``Subsession`` and
        ``Group`` model of the same app.
        """
        subsession_model = '{app_label}.Subsession'.format(
            app_label=cls._meta.app_label)
        subsession_field = models.ForeignKey(subsession_model, on_delete=models.CASCADE)
        ensure_field(cls, 'subsession', subsession_field)

        group_model = '{app_label}.Group'.format(
            app_label=cls._meta.app_label)
        group_field = models.ForeignKey(group_model, null=True, on_delete=models.CASCADE)
        ensure_field(cls, 'group', group_field)
        import model_utils

        add_field_tracker(cls)
