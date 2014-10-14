# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
from otree import widgets
from otree.common import Money, money_range
import random
# </standard imports>

doc = """
In a common value auction game, players simultaneously bid on the item being auctioned.
Prior to bidding, they are given an estimate of the actual value of the item. This actual value is revealed after the bidding.
Bids are private. The player with the highest bid wins the auction, but payoff depends on the bid amount and the actual value.
Source code <a href="https://github.com/oTree-org/oTree/tree/master/common_value_auction" target="_blank">here</a>.
"""

class Constants:
    min_allowable_bid = Money(0.0)
    max_allowable_bid = Money(10.0)

    # Error margin for the value estimates shown to the players
    estimate_error_margin = Money(1.00)

class Subsession(otree.models.BaseSubsession):

    name_in_url = 'common_value_auction'

    def highest_bid(self):
        return max([p.bid_amount for p in self.get_players()])

    def set_winner(self):
        players_with_highest_bid = [p for p in self.get_players() if p.bid_amount == self.highest_bid()]
        winner = random.choice(players_with_highest_bid)    # if tie, winner is chosen at random
        winner.is_winner = True

    item_value = models.MoneyField(
        default=lambda: round(random.uniform(Constants.min_allowable_bid, Constants.max_allowable_bid), 1),
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




class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_group = 1


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    item_value_estimate = models.MoneyField(
        doc="""Estimate of the common value, may be different for each player"""
    )

    bid_amount = models.MoneyField(
        doc="""Amount bidded by the player"""
    )

    def bid_amount_error_message(self, value):
        if not Constants.min_allowable_bid <= value <= Constants.max_allowable_bid:
            return 'The amount bidded must be between {} and {}, inclusive.'.format(Constants.min_allowable_bid, Constants.max_allowable_bid)

    is_winner = models.BooleanField(
        default=False,
        doc="""Indicates whether the player is the winner"""
    )

    def set_payoff(self):
        if self.is_winner:
            self.payoff = self.subsession.item_value - self.bid_amount
            if self.payoff < 0:
                self.payoff = 0
        else:
            self.payoff = 0