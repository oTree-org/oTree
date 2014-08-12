# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-otree-docs/wiki"""

from otree.db import models
import otree.models
from otree.common import Money, money_range
import random


doc = """
In Private Value Auction Game. Consists of multiple players. Each player submits a
bid for a prize being sold in an auction. The prize value is privately known to each player and therefore
uncertainty on the other player's value. The winner is the player with the highest bid value.

<p>Source code <a href="https://github.com/wickens/otree_library/tree/master/private_value_auction">here</a></p>
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'private_value_auction'

    def choose_winner(self):
        highest_bid = max(p.bid_amount for p in self.players)
        # could be a tie
        players_with_highest_bid = [p for p in self.players if p.bid_amount == highest_bid]
        random_highest_bidder = random.choice(players_with_highest_bid)
        random_highest_bidder.is_winner = True


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
        return money_range(0, self.treatment.price_value-0.2, 0.05) # range less than price value **uncertain aspect


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

    def other_player(self):
        """Returns other player in match"""
        return self.other_players_in_match()[0]

    def set_payoff(self):
        if self.is_winner:
            self.payoff = self.treatment.price_value - self.bid_amount
        else:
            self.payoff = 0


def treatments():
    return [Treatment.create()]