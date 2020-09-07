from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


doc = """
In this Vickrey auction, 3 players bid for an object with private values. Each
player can only submit one bid.

See: Vickrey, William. "Counterspeculation, auctions, and competitive '
sealed tenders." The Journal of finance 16.1 (1961): 8-37.
"""


class Constants(BaseConstants):
    name_in_url = 'vickrey_auction'
    players_per_group = 3
    num_rounds = 1

    instructions_template = 'vickrey_auction/Instructions.html'

    endowment = c(100)


class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            p.private_value = random.randint(0, Constants.endowment)


class Group(BaseGroup):
    highest_bid = models.CurrencyField()
    second_highest_bid = models.CurrencyField()

    def set_payoffs(self):
        players = self.get_players()
        bids = sorted([p.bid_amount for p in players], reverse=True)
        self.highest_bid = bids[0]
        self.second_highest_bid = bids[1]
        players_with_highest_bid = [
            p for p in players
            if p.bid_amount == self.highest_bid
            ]
        # if tie, winner is chosen at random
        winner = random.choice(players_with_highest_bid)
        winner.is_winner = True
        for p in players:
            p.payoff = Constants.endowment
            if p.is_winner:
                p.payoff += (p.private_value - self.second_highest_bid)


class Player(BasePlayer):
    private_value = models.CurrencyField(
        doc="How much the player values the item, generated randomly"
    )

    bid_amount = models.CurrencyField(
        min=0, max=Constants.endowment,
        doc="Amount bidded by the player"
    )

    is_winner = models.BooleanField(
        initial=False,
        doc="""Indicates whether the player is the winner"""
    )
