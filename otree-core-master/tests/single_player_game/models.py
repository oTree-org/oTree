# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
import otree.constants
from otree.common import Currency as c
# </standard imports>


class Constants(otree.constants.BaseConstants):
    name_in_url = 'simple_game'
    players_per_group = None
    num_rounds = 1


class Subsession(otree.models.BaseSubsession):

    def before_session_starts(self):
        self.session.vars['a'] = 1
        if self.round_number == 1:
            for p in self.get_players():
                p.participant.vars['a'] = 1
            for g in self.get_groups():
                for p2 in g.get_players():
                    p2.participant.vars['b'] = 1
        for p3 in self.get_players():
            p3.in_before_session_starts = 1
        for g2 in self.get_groups():
            g2.in_before_session_starts = 1


class Group(otree.models.BaseGroup):
    def set_payoffs(self):
        for p in self.get_players():
            p.payoff = c(50)

    # example field
    min_max = models.CurrencyField(
        doc="""
        Description of this field, for documentation
        """,
        min=5,
        max=10
    )

    dynamic_min_max = models.CurrencyField()

    in_before_session_starts = models.CurrencyField()


class Player(otree.models.BasePlayer):

    def other_player(self):
        """Returns other player in group. Only valid for 2-player groups."""
        return self.get_others_in_group()[0]

    blank = models.CharField(blank=True)

    add100_1 = models.PositiveIntegerField()
    add100_2 = models.PositiveIntegerField()

    even_int = models.PositiveIntegerField()

    after_next_button_field = models.BooleanField()

    dynamic_choices = models.CharField()

    dynamic_min_max = models.CurrencyField()

    in_before_session_starts = models.CurrencyField()

    def role(self):
        # you can make this depend of self.id_in_group
        return ''
