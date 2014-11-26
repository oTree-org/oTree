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

    name_in_url = 'ultimatum'
    players_per_group = 2
    number_of_rounds = 1
    endowment = c(100)

class Subsession(otree.models.BaseSubsession):
    pass


    def initialize(self):
        for g in self.get_groups():
            g.strategy = random.choice([True, False])

    def is_valid_amount(self, amount):
        return amount in self.offer_choices()


class Group(otree.models.BaseGroup):

    subsession = models.ForeignKey(Subsession)


    amount_offered = models.CurrencyField()

    offer_accepted = models.NullBooleanField(
        doc="if offered amount is accepted (direct response method)"
    )

    offer_1 = models.NullBooleanField(widget=widgets.RadioSelectHorizontal())
    offer_2 = models.NullBooleanField(widget=widgets.RadioSelectHorizontal())
    offer_3 = models.NullBooleanField(widget=widgets.RadioSelectHorizontal())
    offer_4 = models.NullBooleanField(widget=widgets.RadioSelectHorizontal())
    offer_5 = models.NullBooleanField(widget=widgets.RadioSelectHorizontal())
    offer_6 = models.NullBooleanField(widget=widgets.RadioSelectHorizontal())
    offer_7 = models.NullBooleanField(widget=widgets.RadioSelectHorizontal())
    offer_8 = models.NullBooleanField(widget=widgets.RadioSelectHorizontal())
    offer_9 = models.NullBooleanField(widget=widgets.RadioSelectHorizontal())
    offer_10 = models.NullBooleanField(widget=widgets.RadioSelectHorizontal())
    offer_11 = models.NullBooleanField(widget=widgets.RadioSelectHorizontal())

    def get_all_offer_fields(self):
        return [self.offer_1, self.offer_2, self.offer_3, self.offer_4, self.offer_5, self.offer_6, self.offer_7, self.offer_8, self.offer_9, self.offer_10, self.offer_11]

    def set_payoffs(self):
        p1, p2 = self.get_players()
        if self.offer_accepted:
            p1.payoff = Constants.endowment - self.amount_offered
            p2.payoff = self.amount_offered
        else:
            p1.payoff = 0
            p2.payoff = 0


class Player(otree.models.BasePlayer):

    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)


