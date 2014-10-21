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
In a private value auction game, players simultaneously bid on the item being auctioned.
Each player knows only their private value of the item. The actual value of the item is not known.
Bids are private. The player with the highest bid wins the auction, but payoff depends on the bid amount and the private value.
Source code <a href="https://github.com/oTree-org/oTree/tree/master/private_value_auction" target="_blank">here</a>.
"""

class Constants:
    min_allowable_bid = Money(0.0)
    max_allowable_bid = Money(10.0)


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'private_value_auction'





class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_group = 2


    def highest_bid(self):
        return max([p.bid_amount for p in self.get_players()])


    def set_winner(self):
        players_with_highest_bid = [p for p in self.get_players() if p.bid_amount == self.highest_bid()]
        winner = random.choice(players_with_highest_bid)    # if tie, winner is chosen at random
        winner.is_winner = True


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    private_value = models.MoneyField(
        doc="""How much the player values the item, generated randomly"""
    )

    bid_amount = models.MoneyField(
        default=None,
        doc="""Amount bidded by the player"""
    )

    def bid_amount_choices(self):
        return money_range(Constants.min_allowable_bid, Constants.max_allowable_bid, 0.05)

    is_winner = models.BooleanField(
        default=False,
        doc="""Indicates whether the player is the winner"""
    )

    def generate_private_value(self):
        return round(random.uniform(Constants.min_allowable_bid, Constants.max_allowable_bid), 1)

    def set_payoff(self):
        if self.is_winner:
            self.payoff = self.private_value - self.bid_amount
            if self.payoff < 0:
                self.payoff = 0
        else:
            self.payoff = 0


