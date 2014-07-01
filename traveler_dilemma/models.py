# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-ptree-docs/wiki"""

from ptree.db import models
import ptree.models
from ptree.common import currency

doc = """
Traveler's dilemma game. Single treatment.
Both players make a claim at the same time.
"""


class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'traveler_dilemma'


class Treatment(ptree.models.BaseTreatment):
    subsession = models.ForeignKey(Subsession)

    reward = models.PositiveIntegerField(null=True,
                       doc="""Player's reward for the lowest claim""")

    penalty = models.PositiveIntegerField(null=True,
                       doc="""Player's deduction for the higher claim""")

    max_amount = models.PositiveIntegerField(null=True,
                        doc="""The maximum claim to be requested""")
    min_amount = models.PositiveIntegerField(null=True,
                        doc="""The minimum claim to be requested""")


class Match(ptree.models.BaseMatch):

    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)

    participants_per_match = 2

    def claim_choices(self):
        """Range of allowed claim values"""
        return range(self.treatment.min_amount, self.treatment.max_amount + 1, 5)

    def get_claim_field_choices(self):
        """A tuple of allowed claim estimates"""
        return tuple([(i, currency(i)) for i in self.claim_choices()])


class Participant(ptree.models.BaseParticipant):

    match = models.ForeignKey(Match, null = True)
    treatment = models.ForeignKey(Treatment, null = True)
    subsession = models.ForeignKey(Subsession)

    # claim by participant
    claim = models.PositiveIntegerField(
        null=True,
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

    treatment_list = []

    treatment = Treatment(
        reward=10,
        penalty=10,
        max_amount=100,
        min_amount=20,
    )

    treatment_list.append(treatment)

    return treatment_list