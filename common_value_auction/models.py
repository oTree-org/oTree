from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

doc = """
In a common value auction game, players simultaneously bid on the item being
auctioned.<br/>
Prior to bidding, they are given an estimate of the actual value of the item.
This actual value is revealed after the bidding.<br/>
Bids are private. The player with the highest bid wins the auction, but
payoff depends on the bid amount and the actual value.<br/>
"""


class Constants(BaseConstants):
    name_in_url = 'common_value_auction'
    players_per_group = None
    num_rounds = 1

    instructions_template = 'common_value_auction/instructions.html'

    min_allowable_bid = c(0)
    max_allowable_bid = c(10)

    # Error margin for the value estimates shown to the players
    estimate_error_margin = c(1)


class Subsession(BaseSubsession):
    def creating_session(self):
        for g in self.get_groups():
            item_value = random.uniform(
                Constants.min_allowable_bid,
                Constants.max_allowable_bid
            )
            g.item_value = round(item_value, 1)


class Group(BaseGroup):
    item_value = models.CurrencyField(
        doc="""Common value of the item to be auctioned, random for treatment"""
    )

    highest_bid = models.CurrencyField()

    def set_winner(self):
        players = self.get_players()
        self.highest_bid = max([p.bid_amount for p in players])

        players_with_highest_bid = [p for p in players if p.bid_amount == self.highest_bid]
        winner = random.choice(
            players_with_highest_bid)  # if tie, winner is chosen at random
        winner.is_winner = True

    def generate_value_estimate(self):
        minimum = self.item_value - Constants.estimate_error_margin
        maximum = self.item_value + Constants.estimate_error_margin
        estimate = random.uniform(minimum, maximum)

        estimate = round(estimate, 1)

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
