# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
from otree import widgets
from otree.common import Currency as c, currency_range
import random
# </standard imports>

doc="""
Ultimatum game with two treatments: direct response and strategy method.
In the former, one player makes an offer and the other either accepts or rejects.
It comes in two flavors, with and without hypothetical questions about the second player's response to offers other than the one that is made.
In the latter treatment, the second player is given a list of all possible offers, and is asked which ones to accept or reject.
"""

class Constants:

    name_in_url = 'ultimatum_demo'
    players_per_group = 2
    num_rounds = 1

    endowment = c(100)
    payoff_if_rejected = c(0)


class Subsession(otree.models.BaseSubsession):
    pass


class Group(otree.models.BaseGroup):

    subsession = models.ForeignKey(Subsession)

    amount_offered = models.CurrencyField(min=0, max = Constants.endowment)

    offer_accepted = models.BooleanField(
        doc="if offered amount is accepted (direct response method)"
    )



    def set_payoffs(self):
        p1, p2 = self.get_players()


        if self.offer_accepted:
            p1.payoff = Constants.endowment - self.amount_offered
            p2.payoff = self.amount_offered
        else:
            p1.payoff = Constants.payoff_if_rejected
            p2.payoff = Constants.payoff_if_rejected


class Player(otree.models.BasePlayer):

    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)


