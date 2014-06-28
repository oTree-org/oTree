# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-ptree-docs/wiki"""

from ptree.db import models
import ptree.models
from ptree.common import currency

doc = """
Traveler's Dilemma Game involves two participants:
Assuming, both participants have lost two identical items.
Both participants are going to be compensated for their lost items but they have to estimate the value of
their items without conferring with each another.
"""


class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'travelers_dilemma'


class Treatment(ptree.models.BaseTreatment):
    subsession = models.ForeignKey(Subsession)

    honesty_gain = models.PositiveIntegerField(null=True,
                       doc="""Player's gain or loss as a result of the value given""")

    max_value = models.PositiveIntegerField(null=True,
                        doc="""The maximum value to be compensated""")
    min_value = models.PositiveIntegerField(null=True,
                        doc="""The minimum value to be compensated""")


class Match(ptree.models.BaseMatch):

    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)

    participants_per_match = 2

    def value_choices(self):
        """Range of allowed estimate values"""
        return range(self.treatment.min_value, self.treatment.max_value + 1, 5)

    def get_value_field_choices(self):
        """A tuple of allowed value estimates"""
        return tuple([(i, currency(i)) for i in self.value_choices()])


class Participant(ptree.models.BaseParticipant):

    match = models.ForeignKey(Match, null = True)
    treatment = models.ForeignKey(Treatment, null = True)
    subsession = models.ForeignKey(Subsession)

    # estimated value by participant
    estimate_value = models.PositiveIntegerField(
        null=True,
        doc="""
        Each player's estimated value of their items
        """
    )

    def other_participant(self):
        return self.other_participants_in_match()[0]

    def set_payoff(self):
        if self.estimate_value < self.other_participant().estimate_value:
            self.payoff = self.estimate_value + self.treatment.honesty_gain
            self.other_participant().payoff = self.other_participant().estimate_value - self.treatment.honesty_gain
        elif self.estimate_value > self.other_participant().estimate_value:
            self.payoff = self.estimate_value - self.treatment.honesty_gain
            self.other_participant().payoff = self.other_participant().estimate_value + self.treatment.honesty_gain
        else:
            self.payoff = self.other_participant().payoff = self.estimate_value


def treatments():

    treatment_list = []

    treatment = Treatment(
        honesty_gain=10,
        max_value=100,
        min_value=20,
    )

    treatment_list.append(treatment)

    return treatment_list