# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-ptree-docs/wiki"""

from ptree.db import models
import ptree.models
from ptree.common import Money, money_range

author = 'Dev'

doc = """
Tragedy of the commons.

<p>Source code <a href="https://github.com/wickens/ptree_library/tree/master/tragedy_of_the_commons">here</a></p>
"""


class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'tragedy_of_the_commons'


class Treatment(ptree.models.BaseTreatment):
    subsession = models.ForeignKey(Subsession)

    common_gain = models.MoneyField(
        doc="""""",
        default=1.00
    )
    common_loss = models.MoneyField(
        doc="""""",
        default=0.00
    )
    individual_gain = models.MoneyField(
        doc="""""",
        default=2.00
    )
    defect_costs = models.MoneyField(
        doc="""""",
        default=0.20
    )


class Match(ptree.models.BaseMatch):

    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)

    participants_per_match = 2


class Participant(ptree.models.BaseParticipant):

    match = models.ForeignKey(Match, null = True)
    treatment = models.ForeignKey(Treatment, null = True)
    subsession = models.ForeignKey(Subsession)

    def other_participant(self):
        """Returns other participant in match. Only valid for 2-player matches."""
        return self.other_participants_in_match()[0]

    decision = models.CharField(
        choices = ['cooperate', 'defect'],
        doc="""
        Participants decision: cooperate or Defect
        """
    )

    def set_payoff(self):
        # TODO:
        # - add more participants: currently 2 participants
        # - modify the basic payoff logic
        if self.decision == 'defect' and self.other_participant().decision == 'defect':  # all defect:
            self.payoff = self.treatment.common_loss
        elif self.decision == 'cooperate' and self.other_participant().decision == 'cooperate':  # all cooperate
            self.payoff = self.treatment.common_gain
        else:  # some cooperate and others defect
            if self.decision == 'defect':
                # defector
                self.payoff = self.treatment.individual_gain - self.treatment.defect_costs
            elif self.decision == 'cooperate':
                # cooperative
                self.payoff = self.treatment.common_gain - self.treatment.defect_costs


def treatments():
    return [Treatment.create()]