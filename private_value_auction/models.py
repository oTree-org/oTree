# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-ptree-docs/wiki"""

from ptree.db import models
import ptree.models
from ptree.common import currency
import random


doc = """
In Private Value Auction Game. There are two participants anonymously paired. Each of the participants will submit a
bid for a prize being sold in an auction. The winner is the participant with the highest bid value.
"""


class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'private_value_auction'


class Treatment(ptree.models.BaseTreatment):
    subsession = models.ForeignKey(Subsession)

    price_value = models.PositiveIntegerField(
        null=True,
        doc="""
        Price value of the prize being sold in the auction
        """
    )


class Match(ptree.models.BaseMatch):

    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)

    participants_per_match = 2

    def bid_choices(self):
        """Range of allowed bid values"""
        return range(0, self.treatment.price_value + 1, 5)

    def get_bid_field_choices(self):
        """A tuple of allowed bid values"""
        return tuple([(i, currency(i)) for i in self.bid_choices()])


class Participant(ptree.models.BaseParticipant):

    match = models.ForeignKey(Match, null = True)
    treatment = models.ForeignKey(Treatment, null = True)
    subsession = models.ForeignKey(Subsession)

    bid_amount = models.PositiveIntegerField(
        null=True,
        doc="""
        Amount bidded by each participant
        """
    )
    is_winner = models.BooleanField(
        default=False,
        doc="""
        Indicates whether the participant is the winner or not
        """
    )

    def other_participant(self):
        """Returns other participant in match"""
        return self.other_participants_in_match()[0]

    def set_payoff(self):
        if self.bid_amount > self.other_participant().bid_amount:
            self.is_winner = True
            self.payoff = self.treatment.price_value - self.bid_amount
        elif self.bid_amount < self.other_participant().bid_amount:
            self.other_participant().is_winner = True
            self.payoff = 0
        else:
            if self.payoff is None:
                random_winner = random.choice(range(1, self.match.participants_per_match+1))
                if random_winner == self.index_among_participants_in_match:
                    self.payoff = self.bid_amount
                    self.other_participants_in_match().payoff = 0


def treatments():

    treatment_list = []

    treatment = Treatment(
        price_value=200,
    )

    treatment_list.append(treatment)

    return treatment_list