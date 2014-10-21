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
Lemon market.
"""

class Constants:
    max_bid_amount = Money(1.00)


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'lemon_market'





class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    bid_amount = models.MoneyField(
        doc="""
        Amount bidded by the bidder
        """
    )
    random_value = models.MoneyField(
        doc="""
        Random value for the value of commodity to be auctioned.
        """
    )

    players_per_group = 1

    def calculate_value(self):
        self.random_value = random.choice(money_range(0.00, 1.00))

    def bid_amount_choices(self):
        return money_range(0, Constants.max_bid_amount, 0.05)


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    def set_payoff(self):
        self.group.calculate_value()
        if self.group.bid_amount > self.group.random_value:
            self.payoff = 0
        else:
            self.payoff = (1.5 * Constants.max_bid_amount) - self.group.bid_amount


