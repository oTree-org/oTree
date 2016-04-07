# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer

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

class Constants(BaseConstants):

    name_in_url = 'ultimatum'
    players_per_group = 2
    num_rounds = 1

    endowment = c(100)
    payoff_if_rejected = c(0)
    offer_increment = c(10)

    offer_choices = currency_range(0, endowment, offer_increment)
    offer_choices_count = len(offer_choices)

    keep_give_amounts = []
    for offer in offer_choices:
        keep_give_amounts.append((offer, endowment - offer))


class Subsession(BaseSubsession):

    def before_session_starts(self):
        # randomize to treatments
        for g in self.get_groups():
            if 'treatment' in self.session.config:
                g.strategy = self.session.config['treatment'] == 'strategy'
            else:
                g.strategy = random.choice([True, False])


class Group(BaseGroup):

    strategy = models.BooleanField(
        doc="""Whether this group uses strategy method"""
    )

    amount_offered = models.CurrencyField(choices=Constants.offer_choices)

    offer_accepted = models.BooleanField(
        doc="if offered amount is accepted (direct response method)"
    )


    response_0 = models.BooleanField(widget=widgets.RadioSelectHorizontal())
    response_10 = models.BooleanField(widget=widgets.RadioSelectHorizontal())
    response_20 = models.BooleanField(widget=widgets.RadioSelectHorizontal())
    response_30 = models.BooleanField(widget=widgets.RadioSelectHorizontal())
    response_40 = models.BooleanField(widget=widgets.RadioSelectHorizontal())
    response_50 = models.BooleanField(widget=widgets.RadioSelectHorizontal())
    response_60 = models.BooleanField(widget=widgets.RadioSelectHorizontal())
    response_70 = models.BooleanField(widget=widgets.RadioSelectHorizontal())
    response_80 = models.BooleanField(widget=widgets.RadioSelectHorizontal())
    response_90 = models.BooleanField(widget=widgets.RadioSelectHorizontal())
    response_100 = models.BooleanField(widget=widgets.RadioSelectHorizontal())


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


class Player(BasePlayer):

    pass

