# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-otree-docs/wiki"""

from otree.db import models
import otree.models
from otree.common import Money, money_range
import random

author = 'Dev'

doc = """
In Common Value Auction Game, there are multiple players with each player submitting
a bid for a prize being sold in an auction. The prize value is known and same to all players.
The winner is the player with the highest bid value.

Source code <a href="https://github.com/oTree-org/oTree/tree/master/common_value_auction" target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'common_value_auction'

    prize_value = models.MoneyField(
        default=2.00,
        doc="""
        Value of the item to be auctioned.
        """
    )

    def bid_choices(self):
        """Range of allowed bid values"""
        return money_range(0, self.prize_value, 0.05)

    def set_payoffs(self):
        highest_bid = max(p.bid_amount for p in self.players)
        # could be a tie
        players_with_highest_bid = [p for p in self.players if p.bid_amount == highest_bid]
        winner = random.choice(players_with_highest_bid)
        winner.is_winner = True
        winner.payoff = self.prize_value - winner.bid_amount
        for p in self.players:
            if not p.is_winner:
                p.payoff = 0


class Treatment(otree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>


class Match(otree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_match = 1


class Player(otree.models.BasePlayer):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    bid_amount = models.MoneyField(
        default=None,
        doc="""
        Amount bidded by the player
        """
    )

    is_winner = models.BooleanField(
        default=False,
        doc="""
        Indicates whether the player is the winner or not
        """
    )

def treatments():
    return [Treatment.create()]