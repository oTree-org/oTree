# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-ptree-docs/wiki"""

from ptree.db import models
import ptree.models
from ptree.common import Money, money_range
import random


doc = """
In Private Value Auction Game. Consists of multiple participants. Each participant submits a
bid for a prize being sold in an auction. The prize value is privately known to each participant and therefore
uncertainty on the other participant's value. The winner is the participant with the highest bid value.

<p>Source code <a href="https://github.com/wickens/ptree_library/tree/master/private_value_auction">here</a></p>
"""


class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'private_value_auction'

    def choose_winner(self):
        highest_bid = max(p.bid_amount for p in self.participants())
        # could be a tie
        participants_with_highest_bid = [p for p in self.participants() if p.bid_amount == highest_bid]
        random_highest_bidder = random.choice(participants_with_highest_bid)
        random_highest_bidder.is_winner = True


class Treatment(ptree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    price_value = models.MoneyField(
        default=2.00,
        doc="""
        Price value of the prize being sold in the auction
        """
    )


class Match(ptree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    participants_per_match = 1

    def bid_choices(self):
        """Range of allowed bid values"""
        return money_range(0, self.treatment.price_value-0.2, 0.05) # range less than price value **uncertain aspect


class Participant(ptree.models.BaseParticipant):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    bid_amount = models.MoneyField(
        default=None,
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
        if self.is_winner:
            self.payoff = self.treatment.price_value - self.bid_amount
        else:
            self.payoff = 0


def treatments():
    return [Treatment.create()]