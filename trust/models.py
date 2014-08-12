# -*- coding: utf-8 -*-
from otree.db import models
import otree.models
from otree.common import money_range


doc = """
Trust game. Single treatment. Both players are given an initial sum.
One player may give part of the sum to the other player, who actually receives triple the amount.
The second player may then give part of the now-tripled amount back to the first player.
Source code <a href="https://github.com/oTree-org/oTree/tree/master/trust" target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'trust'


class Treatment(otree.models.BaseTreatment):

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


class Match(otree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_match = 2

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

    def set_payoffs(self):
        p1 = self.get_player_by_index(1)
        p2 = self.get_player_by_index(2)

        p1.payoff = self.treatment.amount_allocated - self.sent_amount + self.sent_back_amount
        p2.payoff = self.treatment.amount_allocated + self.sent_amount * 3 - self.sent_back_amount

class Player(otree.models.BasePlayer):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

def treatments():

    return [Treatment.create()]
