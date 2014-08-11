# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-ptree-docs/wiki"""

from ptree.db import models
import ptree.models
from ptree.common import Money, money_range

doc = """
Traveler's dilemma game has two participants.
Each participant is told to make a claim. Payoffs calculated according to the claims made.

<p>Source code <a href="https://github.com/wickens/ptree_library/tree/master/traveler_dilemma">here</a></p>
"""


class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'traveler_dilemma'


class Treatment(ptree.models.BaseTreatment):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    reward = models.MoneyField(default=0.10,
                       doc="""Player's reward for the lowest claim""")

    penalty = models.MoneyField(default=0.10,
                       doc="""Player's deduction for the higher claim""")

    max_amount = models.MoneyField(default=1.00,
                        doc="""The maximum claim to be requested""")
    min_amount = models.MoneyField(default=0.20,
                        doc="""The minimum claim to be requested""")


class Match(ptree.models.BaseMatch):
    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    participants_per_match = 2

    def claim_choices(self):
        """Range of allowed claim values"""
        return money_range(self.treatment.min_amount, self.treatment.max_amount, 0.05)


class Participant(ptree.models.BaseParticipant):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    # claim by participant
    claim = models.MoneyField(
        default=None,
        doc="""
        Each participant's claim
        """
    )

    def other_participant(self):
        return self.other_participants_in_match()[0]

    def set_payoff(self):
        if self.claim < self.other_participant().claim:
            self.payoff = self.claim + self.treatment.reward
        elif self.claim > self.other_participant().claim:
            self.payoff = self.claim - self.treatment.penalty
        else:
            self.payoff = self.claim


def treatments():
    return [Treatment.create()]