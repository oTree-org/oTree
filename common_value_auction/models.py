# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-otree-docs/wiki"""

from otree.db import models
import otree.models
from otree.common import Money, money_range
import random

author = 'Dev'

doc = """
In Common Value Auction Game, there are multiple participants with each participant submitting
a bid for a prize being sold in an auction. The prize value is known and same to all participants.
The winner is the participant with the highest bid value.

<p>Source code <a href="https://github.com/wickens/otree_library/tree/master/common_value_auction">here</a></p>
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'common_value_auction'

    def choose_winner(self):
        highest_bid = max(p.bid_amount for p in self.participants())
        # could be a tie
        participants_with_highest_bid = [p for p in self.participants() if p.bid_amount == highest_bid]
        random_highest_bidder = random.choice(participants_with_highest_bid)
        random_highest_bidder.is_winner = True


class Treatment(otree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    prize_value = models.MoneyField(
        default=2.00,
        doc="""
        Value of the item to be auctioned.
        """
    )


class Match(otree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    participants_per_match = 2

    def bid_choices(self):
        """Range of allowed bid values"""
        return money_range(0, self.treatment.prize_value, 0.05)


class Participant(otree.models.BaseParticipant):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    bid_amount = models.MoneyField(
        default=None,
        doc="""
        Amount bidded by the participant
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
            self.payoff = self.treatment.prize_value - self.bid_amount
        else:
            self.payoff = 0


def treatments():
    return [Treatment.create()]