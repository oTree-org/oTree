# -*- coding: utf-8 -*-
from ptree.db import models
import ptree.models
from ptree.common import money_range


doc = """
Trust game. Single treatment. Both players are given an initial sum.
One player may give part of the sum to the other player, who actually receives triple the amount.
The second player may then give part of the now-tripled amount back to the first player.
Source code <a href="https://github.com/wickens/ptree_library/tree/master/trust" target="_blank">here</a>.
"""


class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'trust'


class Treatment(ptree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    amount_allocated = models.MoneyField(
        default=1.00,
        doc="""Initial amount allocated to each player"""
    )

    increment_amount = models.MoneyField(
        default=0.05,
        doc="""The increment between amount choices"""
    )


class Match(ptree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    participants_per_match = 2

    sent_amount = models.MoneyField(
        default=None,
        doc="""Amount sent by P1""",
        choices=money_range(0, 1, 0.05),
    )

    sent_back_amount = models.MoneyField(
        default=None,
        doc="""Amount sent back by P2""",
    )

    def send_choices(self):
        """Range of allowed values during send"""
        return money_range(0, self.treatment.amount_allocated, self.treatment.increment_amount)

    def send_back_choices(self):
        """Range of allowed values during send back"""
        return money_range(0, self.sent_amount * 3, self.treatment.increment_amount)

    def get_payoff_player_1(self):
        """Calculate P1 payoff"""
        return self.treatment.amount_allocated - self.sent_amount + self.sent_back_amount

    def get_payoff_player_2(self):
        """Calculate P2 payoff"""
        return self.treatment.amount_allocated + self.sent_amount * 3 - self.sent_back_amount


class Participant(ptree.models.BaseParticipant):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    def set_payoff(self):
        """Calculate payoff for each player"""
        if self.index_among_participants_in_match == 1:
            self.payoff = self.match.get_payoff_player_1()
        elif self.index_among_participants_in_match == 2:
            self.payoff = self.match.get_payoff_player_2()


def treatments():

    return [Treatment.create()]
