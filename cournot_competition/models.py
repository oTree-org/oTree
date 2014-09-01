# -*- coding: utf-8 -*-
"""Documentation at https://github.com/oTree-org/otree/wiki"""

from otree.db import models
import otree.models


doc = """
Each player represents a firm. The players have to decide simultaneously how many units to manufacture. All firms manufacture the same kind of product.
The unit price will depend on the total number of units produced, which will determine the profits for each player.
Source code <a href="https://github.com/oTree-org/oTree/tree/master/cournot_competition" target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'cournot_competition'


class Treatment(otree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    total_capacity = models.PositiveIntegerField(
        default=60,
        doc="""Combined production capacity of both players (firms)"""
    )

    currency_per_point = models.MoneyField(
        default=0.01,
        doc="""Currency units for a single point"""
    )

    def max_units_per_player(self):
        return self.total_capacity / Match.players_per_match


class Match(otree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    price_in_points = models.PositiveIntegerField(
        default=None,
        doc="""Price of goods: P = 60 - q1 - q2"""
    )

    total_units = models.PositiveIntegerField(
        default=None,
        doc="""Total units produced by all companies"""
    )

    players_per_match = 3

    def set_payoffs(self):
        self.total_units = sum(p.units for p in self.players)
        self.price_in_points = self.treatment.total_capacity - self.total_units
        for p in self.players:
            p.payoff_in_points = self.price_in_points * p.units
            p.payoff = p.payoff_in_points * self.treatment.currency_per_point


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


def treatments():

    return [Treatment.create()]
