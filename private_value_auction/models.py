# -*- coding: utf-8 -*-
"""Documentation at https://github.com/oTree-org/otree/wiki"""

from otree.db import models
import otree.models
from otree.common import Money, money_range
import random


doc = """
In a private value auction game, players simultaneously bid on the item being auctioned.
Each player knows only their private value of the item. The actual value of the item is not known.
Bids are private. The player with the highest bid wins the auction, but payoff depends on the bid amount and the private value.
Source code <a href="https://github.com/oTree-org/oTree/tree/master/private_value_auction" target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'private_value_auction'


class Treatment(otree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    min_allowable_bid = models.MoneyField(
        default=0.0,
        doc="""Minimum value of item"""
    )

    max_allowable_bid = models.MoneyField(
        default=10.0,
        doc="""Maximum value of item"""
    )


class Match(otree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_match = 2


    def highest_bid(self):
        return max([p.bid_amount for p in self.players])


    def set_winner(self):
        players_with_highest_bid = [p for p in self.players if p.bid_amount == self.highest_bid()]
        winner = random.choice(players_with_highest_bid)    # if tie, winner is chosen at random
        winner.is_winner = True


class Player(otree.models.BasePlayer):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    private_value = models.MoneyField(
        default=None,
        doc="""How much the player values the item, generated randomly"""
    )

    bid_amount = models.MoneyField(
        default=None,
        doc="""Amount bidded by the player"""
    )

    def bid_amount_choices(self):
        return money_range(self.treatment.min_allowable_bid, self.treatment.max_allowable_bid, 0.05)

    is_winner = models.BooleanField(
        default=False,
        doc="""Indicates whether the player is the winner"""
    )

    def generate_private_value(self):
        return round(random.uniform(self.treatment.min_allowable_bid, self.treatment.max_allowable_bid), 1)

    def set_payoff(self):
        if self.is_winner:
            self.payoff = self.private_value - self.bid_amount
            if self.payoff < 0:
                self.payoff = 0
        else:
            self.payoff = 0


def treatments():

    return [Treatment.create()]
