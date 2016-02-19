# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random

import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer
# </standard imports>

author = 'Alex'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'reputation'
    players_per_group = 2
    num_rounds = 1

    endowment = c(100)
    multiplication_factor = 4

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):

    sent_amount = models.CurrencyField(min=50, max=Constants.endowment)
    sent_back_amount = models.CurrencyField()
    
    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p1.payoff = Constants.endowment - self.sent_amount + self.sent_back_amount
        p2.payoff = self.sent_amount * Constants.multiplication_factor - self.sent_back_amount


class Player(BasePlayer):
    pass