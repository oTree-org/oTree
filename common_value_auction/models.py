# -*- coding: utf-8 -*-
"""Documentation at https://github.com/oTree-org/otree/wiki"""

from otree.db import models
import otree.models
import random


doc = """
In a common value auction game, players simultaneously bid on the item being auctioned.
Prior to bidding, they are given an estimate of the actual value of the item. This actual value is revealed after the bidding.
Bids are private. The player with the highest bid wins the auction, but payoff depends on the bid amount and the actual value.
Source code <a href="https://github.com/oTree-org/oTree/tree/master/common_value_auction" target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'common_value_auction'

    def highest_bid(self):
        return max([p.bid_amount for p in self.players])

    def set_winner(self):
        players_with_highest_bid = [p for p in self.players if p.bid_amount == self.highest_bid()]
        winner = random.choice(players_with_highest_bid)    # if tie, winner is chosen at random
        winner.is_winner = True


class Treatment(otree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    item_value = models.MoneyField(
        default=None,
        doc="""Common value of the item to be auctioned, random for treatment"""
    )

    min_allowable_bid = models.MoneyField(
        default=None,
        doc="""Minimum value of item"""
    )

    max_allowable_bid = models.MoneyField(
        default=None,
        doc="""Maximum value of item"""
    )

    estimate_error_margin = models.MoneyField(
        default=None,
        doc="""Error margin for the value estimates shown to the players"""
    )

    def generate_value_estimate(self):
        minimum = self.item_value - self.estimate_error_margin
        maximum = self.item_value + self.estimate_error_margin

        estimate = round(random.uniform(minimum, maximum), 1)

        if estimate < self.min_allowable_bid:
            estimate = self.min_allowable_bid
        if estimate > self.max_allowable_bid:
            estimate = self.max_allowable_bid

        return estimate


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

    item_value_estimate = models.MoneyField(
        default=None,
        doc="""Estimate of the common value, may be different for each player"""
    )

    bid_amount = models.MoneyField(
        default=None,
        doc="""Amount bidded by the player"""
    )

    is_winner = models.BooleanField(
        default=False,
        doc="""Indicates whether the player is the winner"""
    )

    def set_payoff(self):
        if self.is_winner:
            self.payoff = self.treatment.item_value - self.bid_amount
            if self.payoff < 0:
                self.payoff = 0
        else:
            self.payoff = 0


def treatments():

    treatment_list = []

    min_value = 0.0
    max_value = 10.0
    random_item_value = round(random.uniform(min_value, max_value), 1)

    treatment = Treatment.create(
        item_value=random_item_value,
        min_allowable_bid=min_value,
        max_allowable_bid=max_value,
        estimate_error_margin=1.0
    )
    treatment_list.append(treatment)

    return treatment_list
