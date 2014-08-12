# -*- coding: utf-8 -*-
from otree.db import models
import otree.models
from otree.common import Money, money_range


doc = """
Public goods game. Single treatment. Four players can contribute to a joint project.
The total contribution is multiplied by some factor, the resulting amount is then divided equally between the players.
Source code <a href="https://github.com/wickens/otree_library/tree/master/public_goods" target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'public_goods'


class Treatment(otree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    amount_allocated = models.MoneyField(
        default=3.00,
        doc="""Amount allocated to each player"""
    )

    multiplication_factor = models.FloatField(
        default=1.6,
        doc="""The multiplication factor in group contribution"""
    )

    def contribute_choices(self):
        """Returns a list of allowed values for contribution"""
        return money_range(0, self.amount_allocated, 0.10)


class Match(otree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_match = 4

    contributions = models.MoneyField(
        default=None,
        doc="""Total amount contributed by the group players"""
    )

    individual_share = models.MoneyField(
        default=None,
        doc="""The amount each player in the group receives out of the the total contributed (after multiplication by some factor)"""
    )

    def set_payoffs(self):
        contributions = sum(p.contribution for p in self.players())
        individual_share = contributions * self.treatment.multiplication_factor / self.players_per_match
        for p in self.players():
            p.payoff = (self.treatment.amount_allocated - p.contribution) + individual_share


class Player(otree.models.BasePlayer):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    contribution = models.MoneyField(
        default=None,
        doc="""The amount contributed by the player"""
    )


def treatments():
    return [Treatment.create()]