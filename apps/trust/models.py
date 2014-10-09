# -*- coding: utf-8 -*-
from __future__ import division
from otree.db import models
import otree.models
from otree.common import money_range
from otree import widgets


doc = """
In this one-period implementation, the first mover could give part of her or his endowment to the second mover. 
This amount will be tripled and passed to the second mover, who could return part of her or his possession to the first player.
<br />
Source code <a href="https://github.com/oTree-org/oTree/tree/master/trust" target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'trust'

    amount_allocated = models.MoneyField(
        default=1.00,
        doc="""Initial amount allocated to each player"""
    )

    increment_amount = models.MoneyField(
        default=0.05,
        doc="""The increment between amount choices"""
    )





class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_group = 2

    sent_amount = models.MoneyField(
        default=None,
        doc="""Amount sent by P1""",
    )

    sent_back_amount = models.MoneyField(
        default=None,
        doc="""Amount sent back by P2""",
    )

    def sent_amount_choices(self):
        """Range of allowed values during send"""
        return money_range(0, self.subsession.amount_allocated, self.subsession.increment_amount)

    def sent_back_amount_choices(self):
        """Range of allowed values during send back"""
        return money_range(0, self.sent_amount * 3, self.subsession.increment_amount)

    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)

        p1.payoff = self.subsession.amount_allocated - self.sent_amount + self.sent_back_amount
        p2.payoff = self.subsession.amount_allocated + self.sent_amount * 3 - self.sent_back_amount


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>


