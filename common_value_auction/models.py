# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer

from otree import widgets
from otree.common import Currency as c, currency_range
import random
# </standard imports>

doc = """
In a common value auction game, players simultaneously bid on the item being
auctioned.<br/>
Prior to bidding, they are given an estimate of the actual value of the item.
This actual value is revealed after the bidding.<br/>
Bids are private. The player with the highest bid wins the auction, but
payoff depends on the bid amount and the actual value.<br/>
"""

source_code = "https://github.com/oTree-org/oTree/tree/master/common_value_auction"

bibliography = ()

links = {
    "Wikipedia": {
        "Common Value Auction":
            "http://en.wikipedia.org/wiki/Common_value_auction"
    }
}

keywords = ("Common Value Auction",)


class Constants(BaseConstants):
    name_in_url = 'common_value_auction'
    players_per_group = None
    num_rounds = 1

    min_allowable_bid = c(0)
    max_allowable_bid = c(10)

    # Error margin for the value estimates shown to the players
    estimate_error_margin = 1

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):

    def highest_bid(self):
        return max([p.bid_amount for p in self.get_players()])

    def set_winner(self):
        players_with_highest_bid = [p for p in self.get_players() if p.bid_amount == self.highest_bid()]
        winner = random.choice(players_with_highest_bid)    # if tie, winner is chosen at random
        winner.is_winner = True

    item_value = models.CurrencyField(
        initial=lambda: round(random.uniform(Constants.min_allowable_bid, Constants.max_allowable_bid), 1),
        doc="""Common value of the item to be auctioned, random for treatment"""
    )


    def generate_value_estimate(self):
        minimum = self.item_value - Constants.estimate_error_margin
        maximum = self.item_value + Constants.estimate_error_margin

        estimate = round(random.uniform(minimum, maximum), 1)

        if estimate < Constants.min_allowable_bid:
            estimate = Constants.min_allowable_bid
        if estimate > Constants.max_allowable_bid:
            estimate = Constants.max_allowable_bid

        return estimate


class Player(BasePlayer):

    item_value_estimate = models.CurrencyField(
        doc="""Estimate of the common value, may be different for each player"""
    )

    bid_amount = models.CurrencyField(
        min=Constants.min_allowable_bid, max=Constants.max_allowable_bid,
        doc="""Amount bidded by the player"""
    )

    is_winner = models.BooleanField(
        initial=False,
        doc="""Indicates whether the player is the winner"""
    )

    def set_payoff(self):
        if self.is_winner:
            self.payoff = self.group.item_value - self.bid_amount
            if self.payoff < 0:
                self.payoff = 0
        else:
            self.payoff = 0
