# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-ptree-docs/wiki"""

from ptree.db import models
import ptree.models
import random
from ptree.common import Money, money_range


doc = """
Lemon market.
"""


class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'lemon_market'


class Treatment(ptree.models.BaseTreatment):
    subsession = models.ForeignKey(Subsession)

    max_bid_amount = models.MoneyField(
        null=True,
        doc="""
        Maximum allowed bid amount.
        """
    )


class Match(ptree.models.BaseMatch):

    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)

    bid_amount = models.MoneyField(
        null=True,
        doc="""
        Amount bidded by the bidder
        """
    )
    random_value = models.MoneyField(
        null=True,
        doc="""
        Random value for the value of commodity to be auctioned.
        """
    )

    participants_per_match = 1

    def calculate_value(self):
        self.random_value = random.choice(money_range(0.00, 1.00))


class Participant(ptree.models.BaseParticipant):

    match = models.ForeignKey(Match, null = True)
    treatment = models.ForeignKey(Treatment, null = True)
    subsession = models.ForeignKey(Subsession)

    def set_payoff(self):
        self.match.calculate_value()
        if self.match.bid_amount > self.match.random_value:
            self.payoff = 0
        else:
            self.payoff = (1.5 * self.treatment.max_bid_amount) - self.match.bid_amount


def treatments():
    return [Treatment.create(
        max_bid_amount = 1.00,
    )]