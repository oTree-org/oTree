# -*- coding: utf-8 -*-
"""Documentation at https://github.com/oTree-org/otree/wiki"""

from otree.db import models
import otree.models


doc = """
<p>
In Cournot Competition, players play as firm owners(in duopoly market), each deciding simultaneously on
how much quantity to produce in order to make a profit. Players decide on choosing to maximise their profits or
cooperating with others to improve profits.
</p>
<p>
Source code <a href="https://github.com/oTree-org/oTree/tree/master/cournot_competition">here</a>.
</p>
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'cournot_competition'


class Treatment(otree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    total_capacity = models.PositiveIntegerField(
        default=60,
        doc="""
        Combined production capacity of both players(firms)
        """
    )

    dollars_per_point = models.MoneyField(
        default=0.01,
        doc='Multiply spare units by this factor to determine unit price'
    )

    def max_units_per_player(self):
        return self.total_capacity/Match.players_per_match

class Match(otree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    price_in_points = models.PositiveIntegerField(
        default=None,
        doc="""
        Price of goods: P=60-q1-q2
        """
        )

    total_units = models.PositiveIntegerField(
        default=None,
        doc='''Total units produced by all companies'''
    )

    players_per_match = 3

    def set_payoffs(self):
        self.total_units = sum(p.units for p in self.players)
        self.price_in_points = self.treatment.total_capacity - self.total_units
        for p in self.players:
            p.payoff_in_points = self.price_in_points * p.units
            p.payoff = p.payoff_in_points * self.treatment.dollars_per_point


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
        doc="""
        Quantity of goods to produce.
        """
    )


def treatments():
    return [Treatment.create()]