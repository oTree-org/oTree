# -*- coding: utf-8 -*-
"""Documentation at https://github.com/oTree-org/otree/wiki"""

from otree.db import models
import otree.models
import random


doc = """
In Common Value Auction Game, there are multiple players with each player submitting
a bid for a item being sold in an auction. The item value is known and same to all players.
The winner is the player with the highest bid value.

Source code <a href="https://github.com/oTree-org/oTree/tree/master/common_value_auction" target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'common_value_auction'


class Treatment(otree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    item_value = models.MoneyField(
        default=None,
        doc="""Common value of the item to be auctioned, random for treatment"""
    )

    item_value_min = models.MoneyField(
        default=None,
        doc="""Minimum value of item"""
    )

    item_value_max = models.MoneyField(
        default=None,
        doc="""Maximum value of item"""
    )

    item_value_error_margin = models.MoneyField(
        default=None,
        doc="""Error margin for the value estimates shown to the players"""
    )

    def generate_value_estimate(self):
        minimum = self.item_value - self.item_value_error_margin
        maximum = self.item_value + self.item_value_error_margin

        estimate = round(random.uniform(minimum, maximum), 1)

        if estimate < self.item_value_min:
            estimate = self.item_value_min
        if estimate > self.item_value_max:
            estimate = self.item_value_max

        return estimate

    def set_payoffs(self):
        highest_bid = max(p.bid_amount for p in self.players)
        players_with_highest_bid = [p for p in self.players if p.bid_amount == highest_bid]
        winner = random.choice(players_with_highest_bid)    # if tie, winner is chosen at random
        winner.is_winner = True
        winner.payoff = self.item_value - winner.bid_amount
        for p in self.players:
            if not p.is_winner:
                p.payoff = 0


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


def treatments():

    treatment_list = []

    min_value = 0.0
    max_value = 10.0
    random_item_value = round(random.uniform(min_value, max_value), 1)

    treatment = Treatment.create(
        item_value=random_item_value,
        item_value_min=min_value,
        item_value_max=max_value,
        item_value_error_margin=1.0
    )
    treatment_list.append(treatment)

    return treatment_list
