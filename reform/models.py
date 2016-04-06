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
    pass

class Group(BaseGroup):
    # before any upheavals number of reforms is equal to round number
    def num_reforms(self):
        return self.subsession.round_number

    # pick one player to be reformed
    def reformed_player(self):
        if self.subsession.round_number == 1:
            for p in self.get_players():
                p.reforms = 0
        while True:
            reformed_id = random.randint(1,Constants.players_per_group)
            if self.num_reforms() - self.get_player_by_id(reformed_id).reforms*Constants.players_per_group > 0:
                break
        return reformed_id

    # increase number of reforms by 1 for this player
    def reform(self):
        for p in self.get_players():
            if p.id_in_group == self.reformed_player:
                p.reforms += 1
            else:
                pass


    # base sales + base consumption + number of global reforms passed - number of times player has been reformed * reform penalty
    def payoffs(self):
        for p in self.get_players():
            p.payoff = Constants.base_sales + Constants.base_consumption + self.num_reforms() - p.reforms * Constants.reform_penalty


class Player(BasePlayer):
    pass