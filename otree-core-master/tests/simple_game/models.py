# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.api import (
    BaseSubsession, BaseGroup, BasePlayer, BaseConstants, models
)
# </standard imports>

doc = "foo"

class Constants(BaseConstants):
    name_in_url = 'simple_game_copy'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    players_per_group = None

    def set_payoffs(self):
        for p in self.get_players():
            p.payoff = 0


class Player(BasePlayer):
    my_field = models.CurrencyField()
