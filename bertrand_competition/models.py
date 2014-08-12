# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-otree-docs/wiki"""

from otree.db import models
import otree.models


doc = """
In Bertrand Competition, players play as firm owners(in duopoly market), each deciding simultaneously on how
much price to set for their products. The player with the lowest price carries the day and becomes the winner.

Source code <a href="https://github.com/oTree-org/oTree/tree/master/bertrand_competition" target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'bertrand_competition'


class Treatment(otree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    minimum_price = models.MoneyField(
        default=0.20,
        doc="""
        The minimum price that can be set i.e equivalent to marginal cost.
        """
    )

    maximum_price = models.MoneyField(
        default=1.00,
        doc="""
        The maximum price that can be set .
        """
    )


class Match(otree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_match = 2


class Player(otree.models.BasePlayer):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    price = models.MoneyField(
        default=None,
        doc="""
        The player's target price
        """
    )

    is_winner = models.BooleanField(
        default=False,
        doc="""
        Whether this player is the winner of the match
        """
    )

    def other_player(self):
        '''get the opponent player'''
        return self.other_players_in_match()[0]

    def set_payoff(self):
        if self.price < self.other_player().price:
            self.is_winner = True
            self.payoff = self.price - self.treatment.minimum_price
        elif self.price > self.other_player().price:
            self.payoff = 0
        elif self.price == self.other_player().price:
            self.payoff = (self.price - self.treatment.minimum_price) / 2.0


def treatments():
    return [Treatment.create()]