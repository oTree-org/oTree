# -*- coding: utf-8 -*-
"""Documentation at https://github.com/oTree-org/otree/wiki"""

from otree.db import models
import otree.models
from otree.common import Money, money_range
import random


doc = """
In the private value auction game, each player submits a bid for an item that is being auctioned. The item value is privately known to each player and therefore
uncertainty on the other player's value. The winner is the player with the highest bid value.

Source code <a href="https://github.com/oTree-org/oTree/tree/master/private_value_auction" target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'private_value_auction'

    def set_payoffs(self):
        highest_bid = max([p.bid_amount for p in self.players])
        # could be a tie
        players_with_highest_bid = [p for p in self.players if p.bid_amount == highest_bid]
        random_highest_bidder = random.choice(players_with_highest_bid)
        random_highest_bidder.is_winner = True
        random_highest_bidder.payoff = self.treatment.price_value - self.bid_amount

        for p in self.players:
            if p != random_highest_bidder:
                p.payoff = 0


class Treatment(otree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    price_value = models.MoneyField(
        default=2.00,
        doc="""
        Price value of the prize being sold in the auction
        """
    )


class Match(otree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_match = 1

    def bid_choices(self):
        """Range of allowed bid values"""
        return money_range(0, self.treatment.price_value-0.2, 0.05)     # range less than price value **uncertain aspect


class Player(otree.models.BasePlayer):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    bid_amount = models.MoneyField(
        default=None,
        doc="""
        Amount bidded by each player
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
