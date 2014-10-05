# -*- coding: utf-8 -*-
from __future__ import division
"""Documentation at https://github.com/oTree-org/otree/wiki"""

from otree.db import models
import otree.models


doc = """
In Cournot competition, players simultaneously decide the units of products to manufacture. 
The unit selling price depends on the total units produced. In this implementation, there are 3 firms competing for 1 period.
<br />
Source code <a href="https://github.com/oTree-org/oTree/tree/master/cournot_competition" target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'cournot_competition'

    total_capacity = models.PositiveIntegerField(
        default=60,
        doc="""Total production capacity of all players"""
    )

    currency_per_point = models.MoneyField(
        default=0.01,
        doc="""Currency units for a single point"""
    )

    def max_units_per_player(self):
        return self.total_capacity / Match.players_per_match


class Treatment(otree.models.BaseTreatment):
    """Leave this class empty"""

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>



class Match(otree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    price_in_points = models.PositiveIntegerField(
        default=None,
        doc="""Unit price: P = T - \sum U_i, where T is total capacity and U_i is the number of units produced by player i"""
    )

    total_units = models.PositiveIntegerField(
        default=None,
        doc="""Total units produced by all players"""
    )

    players_per_match = 3

    def set_payoffs(self):
        self.total_units = sum([p.units for p in self.players])
        self.price_in_points = self.subsession.total_capacity - self.total_units
        for p in self.players:
            p.payoff_in_points = self.price_in_points * p.units
            p.payoff = p.payoff_in_points * self.subsession.currency_per_point


class Player(otree.models.BasePlayer):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    payoff_in_points = models.PositiveIntegerField(
        default=None,
    )

    units = models.PositiveIntegerField(
        default=None,
        doc="""Quantity of units to produce"""
    )

    def units_error_message(self, value):
        if not 0 <= value <= self.subsession.max_units_per_player():
            return "The value must be a whole number between {} and {}, inclusive.".format(0, self.subsession.max_units_per_player())

def treatments():

    return [Treatment.create()]
