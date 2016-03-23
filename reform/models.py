# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random

from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer

from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json

# </standard imports>

author = 'Alex'

doc = """
Reputation game
"""

class Constants(BaseConstants):
    name_in_url = 'reform'
    players_per_group = 2
    num_rounds = 1
    base_sales = 16
    base_consumption = 4
    reform_penalty = 4
    reform_benefits = 0.5


class Subsession(BaseSubsession):
    def before_session_starts(self):
        round_number = self.round_number

class Group(BaseGroup):
    def num_reforms(self):
        return self.round_number - 1
    reformed_player = random.randint(1,5)

    def payoffs(self):
        for p in self.get_players():
            p.payoff = Constants.base_sales - p.reforms * Constants.reform_penalty + Constants.base_consumption + self.num_reforms * 0.5


class Player(BasePlayer):
    pass
