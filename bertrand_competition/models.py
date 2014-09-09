# -*- coding: utf-8 -*-
"""Documentation at https://github.com/oTree-org/otree/wiki"""

from otree.db import models
import otree.models

doc = """
In Bertrand Competition, players play as firm owners, each deciding simultaneously on how
much price to set for their products.
The player with the lowest price carries the day and becomes the winner.

Source code <a href="https://github.com/oTree-org/oTree/tree/master/bertrand_competition" target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'bertrand_competition'


class Treatment(otree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    marginal_cost = models.MoneyField(
        default=0.20,
        doc="""Marginal cost of production, effectively the minimum price (exclusive)"""
    )

    maximum_price = models.MoneyField(
        default=1.00,
        doc="""The maximum price"""
    )


class Match(otree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_match = 3

    num_winners = models.PositiveIntegerField(
        default=None,
        doc="""How many players offer lowest price"""
    )

    winning_price = models.MoneyField(
        default=None,
        doc="""Lowest price"""
    )

    def set_payoffs(self):
        self.winning_price = min(p.price for p in self.players)
        self.num_winners = len([p for p in self.players if p.price == self.winning_price])
        winner_payoff = (self.winning_price - self.treatment.marginal_cost) / self.num_winners

        for p in self.players:
            if p.price == self.winning_price:
                p.is_a_winner = True
                p.payoff = winner_payoff
            else:
                p.is_a_winner = False
                p.payoff = 0


class Player(otree.models.BasePlayer):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    price = models.MoneyField(
        default=None,
        doc="""Price player chooses to sell product for"""
    )

    is_a_winner = models.BooleanField(
        default=False,
        doc="""Whether this player offered lowest price"""
    )

    def is_sole_winner(self):
        return self.is_a_winner and self.match.num_winners == 1

    def is_shared_winner(self):
        return self.is_a_winner and self.match.num_winners > 1


def treatments():

    return [Treatment.create()]
