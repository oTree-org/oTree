# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
from otree import widgets
from otree.common import Currency as c, currency_range
import random
# </standard imports>


doc = """
In this Vickrey auction, 3 players bid for an object with private values. Each
player can only submit one bid.

"""


source_code = "https://github.com/oTree-org/oTree/tree/master/vickrey_auction"


bibliography = (
    (
        'Vickrey, William. "Counterspeculation, auctions, and competitive '
        'sealed tenders." The Journal of finance 16.1 (1961): 8-37'
    ),
)


links = {
    "Wikipedia": {
        "Vickrey Auction": "http://en.wikipedia.org/wiki/Vickrey_auction",
        "Generalized Second-Price Auction":
            "http://en.wikipedia.org/wiki/Generalized_second-price_auction",
        "Auction": "http://en.wikipedia.org/wiki/Auction",
    }
}


keywords = (
    "Auction", "Second-Price Auction",
    "Vickrey Auction", "Sealed-Bid Auction"
)


class Constants:
    name_in_url = 'vickrey_auction'
    players_per_group = 3
    num_rounds = 1

    fixed_payoff = c(100)
    min_allowable_bid = c(0)
    max_allowable_bid = c(100)

    training_question_1_my_payoff_limit = c(100) * players_per_group
    training_question_1_my_payoff_correct = c(105)


class Subsession(otree.models.BaseSubsession):
    pass

class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    def highest_bid(self):
        return max([p.bid_amount for p in self.get_players()])

    def second_highest_bid(self):
        values = sorted(
            (p.bid_amount for p in self.get_players()), reverse=True
        )
        return values[1]

    def set_winner(self):
        players_with_highest_bid = [
            p for p in self.get_players()
            if p.bid_amount == self.highest_bid()
        ]
        # if tie, winner is chosen at random
        winner = random.choice(players_with_highest_bid)
        winner.is_winner = True


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    private_value = models.CurrencyField(
        null=True,
        doc="How much the player values the item, generated randomly"
    )

    bid_amount = models.CurrencyField(
        null=True,
        min=Constants.min_allowable_bid, max=Constants.max_allowable_bid,
        doc="Amount bidded by the player"
    )

    is_winner = models.BooleanField(
        initial=False,
        doc="""Indicates whether the player is the winner"""
    )

    training_question_1_my_payoff = models.CurrencyField()

    def is_training_question_1_my_payoff_correct(self):
        return (self.training_question_1_my_payoff==
                Constants.training_question_1_my_payoff_correct)

    def generate_private_value(self):
        return random.randint(
            Constants.min_allowable_bid, Constants.max_allowable_bid
        )

    def set_payoff(self):
        self.payoff = Constants.fixed_payoff
        if self.is_winner:
            self.payoff += (
                self.private_value - self.group.second_highest_bid()
            )
            if self.payoff < 0:
                self.payoff = 0
