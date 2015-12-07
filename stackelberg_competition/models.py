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
In Stackelberg competition, firms decide sequentially on how many units to
produce. The unit selling price depends on the total units produced.
In this one-period implementation, the order of play is randomly determined.
"""


source_code = "https://github.com/oTree-org/oTree/tree/master/stackelberg_competition"


bibliography = ()


links = {
    "Wikipedia": {
        "Stackelberg Competition":
            "https://en.wikipedia.org/wiki/Stackelberg_competition"
    }
}


keywords = ("Stackelberg Competition",)


class Constants(BaseConstants):
    name_in_url = 'stackelberg_competition'
    players_per_group = 2
    num_rounds = 1

    # Total production capacity of both players
    total_capacity = 60

    max_units_per_player = int(total_capacity/2)

    fixed_pay = c(50)
    training_1_correct = c(300)

    training_question_1 = "Suppose firm A first decided to produce 20 units. Then firm B would be informed of firm A's production and decided to produce 30 units. What would be the profit for firm B?"

class Subsession(BaseSubsession):

    pass


class Group(BaseGroup):

    price = models.CurrencyField(
        doc="""Unit price: P = T - Q1 - Q2, where T is total capacity and Q_i are the units produced by the players"""
    )


class Player(BasePlayer):

    training_question_1 = models.CurrencyField()

    def is_training_question_1_correct(self):
        return self.training_question_1 == Constants.training_1_correct

    quantity = models.PositiveIntegerField(
        initial=None,
        min=0, max=Constants.max_units_per_player,
        doc="""Quantity of units to produce"""
    )

    def other_player(self):
        return self.get_others_in_group()[0]

    def set_payoff(self):
        self.group.price = Constants.total_capacity - self.quantity - self.other_player().quantity
        self.payoff = self.group.price * self.quantity

