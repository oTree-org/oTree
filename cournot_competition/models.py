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
<p>In Cournot competition, firms simultaneously decide the units of products to manufacture.
The unit selling price depends on the total units produced. In this implementation, there are 2 firms competing for 1 period.</p>
<p>Source code <a href="https://github.com/oTree-org/oTree/tree/master/cournot_competition" target="_blank">here</a>.</p>
"""

class Constants:
    training_1_correct = 300
    players_per_group = 2

    # Total production capacity of all players
    total_capacity = 60
    max_units_per_player = int(total_capacity / players_per_group)


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'cournot_competition'


class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_group = Constants.players_per_group

    price = models.PositiveIntegerField(
        doc="""Unit price: P = T - \sum U_i, where T is total capacity and U_i is the number of units produced by player i"""
    )

    total_units = models.PositiveIntegerField(
        doc="""Total units produced by all players"""
    )

    def set_points(self):
        self.total_units = sum([p.units for p in self.get_players()])
        self.price = Constants.total_capacity - self.total_units
        for p in self.get_players():
            p.points_earned = self.price * p.units


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    training_question_1 = models.PositiveIntegerField(null=True, verbose_name='')

    def is_training_question_1_correct(self):
        return self.training_question_1 == Constants.training_1_correct

    points_earned = models.PositiveIntegerField(
        doc="""."""
    )

    units = models.PositiveIntegerField(
        default=None,
        doc="""Quantity of units to produce"""
    )

    def units_error_message(self, value):
        if not 0 <= value <= Constants.max_units_per_player:
            return "The value must be a whole number between {} and {}, inclusive.".format(0, Constants.max_units_per_player)

    def other_player(self):
        return self.get_others_in_group()[0]

    def set_payoff(self):
        self.payoff = 0

