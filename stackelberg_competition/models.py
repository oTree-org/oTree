# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
from otree import widgets
from otree.common import Money, money_range
import random
# </standard imports>

doc = """
<p>In Stackelberg competition, firms decide sequentially on how many units to produce. The unit selling price depends on the total units produced.
In this one-period implementation, the order of play is randomly determined.</p>
<p>Source code <a href="https://github.com/oTree-org/oTree/tree/master/stackelberg_competition" target="_blank">here</a>.</p>
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'stackelberg_competition'

    total_capacity = models.PositiveIntegerField(
        default=60,
        doc="""Total production capacity of both players"""
    )

    def max_units_per_player(self):
        return int(self.total_capacity / 2)

    training_1_correct = 300


class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_group = 2

    price = models.PositiveIntegerField(
        default=None,
        doc="""Unit price: P = T - Q1 - Q2, where T is total capacity and Q_i are the units produced by the players"""
    )


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    training_question_1 = models.PositiveIntegerField(null=True, verbose_name='')

    def is_training_question_1_correct(self):
        return self.training_question_1 == self.subsession.training_1_correct

    points_earned = models.PositiveIntegerField(
        default=None,
    )

    quantity = models.PositiveIntegerField(
        default=None,
        doc="""Quantity of units to produce"""
    )

    def quantity_error_message(self, value):
        if not 0 <= value <= self.subsession.max_units_per_player():
            return "The value must be an integer between 0 and {}, inclusive.".format(self.subsession.max_units_per_player())

    def other_player(self):
        return self.get_others_in_group()[0]

    def set_points(self):
        self.group.price = self.subsession.total_capacity - self.quantity - self.other_player().quantity
        self.points_earned = self.group.price * self.quantity

    def set_payoff(self):
        self.payoff = 0
