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
In this Vickrey auction, 3 players bid for an object with private values. Each player can only submit one
bid.
<br/>
Source code <a href="https://github.com/oTree-org/oTree/tree/master/private_value_auction" target="_blank">here</a>.

<h3>Recommended Literature</h3>
<ul>
    <li>Vickrey, William. "Counterspeculation, auctions, and competitive sealed tenders." The Journal of finance 16.1 (1961): 8-37.</li>
</ul>

<p>
    <strong>Wikipedia:</strong>
    <a target="_blank" href="http://en.wikipedia.org/wiki/Vickrey_auction">Vickrey Auction</a>,&nbsp
    <a target="_blank" href="http://en.wikipedia.org/wiki/Generalized_second-price_auction">Generalized Second-Price Auction</a>
    <a target="_blank" href="http://en.wikipedia.org/wiki/Auction">Auction</a>
</p>

<p>
    <strong>Keywords:</strong>
    <a target="_blank" href="https://duckduckgo.com/?q=Auction+game+theory&t=otree"</a>
        <span class="badge">Auction</span>
    </a>,
    <a target="_blank" href="https://duckduckgo.com/?q=Second-Price+Auction+game+theory&t=otree"</a>
        <span class="badge">Second-Price Auction</span>
    </a>,
    <a target="_blank" href="https://duckduckgo.com/?q=Vickrey+Auction+game+theory&t=otree"</a>
        <span class="badge"> Vickrey Auction</span>
    </a>,
    <a target="_blank" href="https://duckduckgo.com/?q=Sealed-Bid+Auction+game+theory&t=otree"</a>
        <span class="badge">Sealed-Bid Auction</span>
    </a>
</p>

"""

class Constants:
    name_in_url = 'private_value_auction'
    players_per_group = 3
    number_of_rounds = 1

    base_payoff = 100
    min_allowable_bid = 0
    max_allowable_bid = 100

    training_question_1_my_payoff_limit = 100 * players_per_group
    training_question_1_my_payoff_correct = 105


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

    private_value = models.PositiveIntegerField(
        null=True,
        doc="How much the player values the item, generated randomly"
    )

    bid_amount = models.PositiveIntegerField(
        null=True, doc="Amount bidded by the player"
    )

    is_winner = models.BooleanField(
        default=False,
        doc="""Indicates whether the player is the winner"""
    )

    training_question_1_my_payoff = models.PositiveIntegerField(
        null=True, verbose_name=''
    )

    def is_training_question_1_my_payoff_correct(self):
        return (self.training_question_1_my_payoff==
                Constants.training_question_1_my_payoff_correct)

    def training_question_1_my_payoff_error_message(self, value):
        is_valid = (
            Constants.min_allowable_bid
            <= value <=
            Constants.training_question_1_my_payoff_limit
        )
        if not is_valid:
            msg = 'The payoff cannot must be in the range [{}, {}]'
            return msg.format(
                Constants.min_allowable_bid,
                Constants.training_question_1_my_payoff_limit
            )

    def bid_amount_error_message(self, value):
        is_valid = (
            Constants.min_allowable_bid <= value <= Constants.max_allowable_bid
        )
        if not is_valid:
            msg = 'The payoff must be in the range [{}, {}]'
            return msg.format(
                Constants.min_allowable_bid, Constants.max_allowable_bid
            )

    def generate_private_value(self):
        return random.randint(
            Constants.min_allowable_bid, Constants.max_allowable_bid
        )

    def set_payoff(self):
        self.payoff = Constants.base_payoff
        if self.is_winner:
            self.payoff += (
                self.private_value - self.group.second_highest_bid()
            )
            if self.payoff < 0:
                self.payoff = 0



