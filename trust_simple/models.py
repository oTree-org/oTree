# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
from otree import widgets
from otree.common import Currency as c, currency_range
import random
# </standard imports>


doc = """
Simple trust game
"""


class Constants:
    name_in_url = 'trust_simple'
    players_per_group = 2
    num_rounds = 1

    endowment = c(10)
    multiplication_factor = 3


class Subsession(otree.models.BaseSubsession):
    pass


class Group(otree.models.BaseGroup):


    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    sent_amount = models.CurrencyField(
        choices=currency_range(0, Constants.endowment, c(1)),
        doc="""Amount sent by P1""",
    )

    sent_back_amount = models.CurrencyField(
        doc="""Amount sent back by P2""",
    )

    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p1.payoff = Constants.endowment - self.sent_amount + self.sent_back_amount
        p2.payoff = self.sent_amount * Constants.multiplication_factor - self.sent_back_amount


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>