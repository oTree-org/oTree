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
    payoff_if_rejected = c(0)
    offer_increment = c(10)

    offer_choices = currency_range(0, endowment, offer_increment)

    keep_give_amounts = [(offer, endowment - offer) for offer in offer_choices]

class Subsession(otree.models.BaseSubsession):

    def initialize(self):
        # randomize to treatments
        for g in self.get_groups():
            g.strategy = random.choice([True, False])


class Group(otree.models.BaseGroup):

    subsession = models.ForeignKey(Subsession)

    strategy = models.NullBooleanField(
        doc="""Whether this group uses strategy method"""
    )

    amount_offered = models.CurrencyField(choices=Constants.offer_choices)

    offer_accepted = models.NullBooleanField(
        doc="if offered amount is accepted (direct response method)"
    )


    response_0 = models.NullBooleanField(widget=widgets.RadioSelectHorizontal())
    response_10 = models.NullBooleanField(widget=widgets.RadioSelectHorizontal())
    response_20 = models.NullBooleanField(widget=widgets.RadioSelectHorizontal())
    response_30 = models.NullBooleanField(widget=widgets.RadioSelectHorizontal())
    response_40 = models.NullBooleanField(widget=widgets.RadioSelectHorizontal())
    response_50 = models.NullBooleanField(widget=widgets.RadioSelectHorizontal())
    response_60 = models.NullBooleanField(widget=widgets.RadioSelectHorizontal())
    response_70 = models.NullBooleanField(widget=widgets.RadioSelectHorizontal())
    response_80 = models.NullBooleanField(widget=widgets.RadioSelectHorizontal())
    response_90 = models.NullBooleanField(widget=widgets.RadioSelectHorizontal())
    response_100 = models.NullBooleanField(widget=widgets.RadioSelectHorizontal())


    def set_payoffs(self):
        p1, p2 = self.get_players()

        if self.strategy:
            self.offer_accepted = getattr(self, 'response_{}'.format(int(self.amount_offered)))

        if self.offer_accepted:
            p1.payoff = Constants.endowment - self.amount_offered
            p2.payoff = self.amount_offered
        else:
            p1.payoff = Constants.payoff_if_rejected
            p2.payoff = Constants.payoff_if_rejected


class Player(otree.models.BasePlayer):

    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)


