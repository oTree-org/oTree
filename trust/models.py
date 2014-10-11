# -*- coding: utf-8 -*-
from __future__ import division
from otree.db import models
import otree.models
from otree.common import money_range
from otree import widgets


doc = """
This is a standard 2-player trust game where the amount sent by player 1 gets tripled. 
The trust game was first proposed by <a href="http://econweb.ucsd.edu/~jandreon/Econ264/papers/Berg%20et%20al%20GEB%201995.pdf" targe="_blank">Berg, Dickhaut, and McCabe (1995)</a>.
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


