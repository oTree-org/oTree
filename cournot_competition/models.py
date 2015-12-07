# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer

from otree import widgets
from otree.common import Currency as c, currency_range
import random
# </standard imports>

doc = """
In Cournot competition, firms simultaneously decide the units of products to
manufacture. The unit selling price depends on the total units produced. In
this implementation, there are 2 firms competing for 1 period.
"""

source_code = "https://github.com/oTree-org/oTree/tree/master/cournot_competition"


bibliography = ()


links = {
    "Wikipedia": {
        "Cournot Competition":
            "https://en.wikipedia.org/wiki/Cournot_competition"
        }
}


keywords = ("Cournot Competition",)


class Constants(BaseConstants):
    name_in_url = 'cournot_competition'
    players_per_group = 2
    num_rounds = 1

    training_1_correct = 300

    base_points = 50
    # Total production capacity of all players
    total_capacity = 60
    max_units_per_player = int(total_capacity / players_per_group)
    feedback1_question = """Suppose firm Q produced 20 units and firm P produced 30 units. What would be the profit for firm P?"""
    feedback1_explanation=  """Total units produced were 20 + 30 = 50. The unit selling price was 60 – 50 = 10. The profit for firm P would be the product of the unit selling price and the unit produced by firm P, that is 10 × 30 = 300"""

class Subsession(BaseSubsession):

    name_in_url = 'cournot_competition'


class Group(BaseGroup):

    price = models.CurrencyField(
        doc="""Unit price: P = T - \sum U_i, where T is total capacity and U_i is the number of units produced by player i"""
    )

    total_units = models.PositiveIntegerField(
        doc="""Total units produced by all players"""
    )

    def set_payoffs(self):
        self.total_units = sum([p.units for p in self.get_players()])
        self.price = Constants.total_capacity - self.total_units
        for p in self.get_players():
            p.payoff = self.price * p.units


class Player(BasePlayer):

    training_question_1 = models.CurrencyField()

    def is_training_question_1_correct(self):
        return self.training_question_1 == Constants.training_1_correct

    units = models.PositiveIntegerField(
        initial=None,
        min=0, max=Constants.max_units_per_player,
        doc="""Quantity of units to produce"""
    )

    def other_player(self):
        return self.get_others_in_group()[0]


