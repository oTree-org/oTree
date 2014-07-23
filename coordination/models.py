# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-ptree-docs/wiki"""

from ptree.db import models
import ptree.models


doc = """
In Coordination game, There are two participants which are required to choose either A or B.
If both Participants chooses the same choice then they both wins, otherwise they loose.

<p>Source code <a href="https://github.com/wickens/ptree_library/tree/master/coordination">here</a></p>
"""


class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'coordination'


class Treatment(ptree.models.BaseTreatment):
    subsession = models.ForeignKey(Subsession)

    similar_amount = models.PositiveIntegerField(
        null=True,
        doc="""
        amount each participant is rewarded for having similar choices
        """
    )

    dissimilar_amount = models.PositiveIntegerField(
        null=True,
        doc="""
        amount each participant is rewarded for having different choices
        """
    )


class Match(ptree.models.BaseMatch):

    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)

    participants_per_match = 2


class Participant(ptree.models.BaseParticipant):

    match = models.ForeignKey(Match, null = True)
    treatment = models.ForeignKey(Treatment, null = True)
    subsession = models.ForeignKey(Subsession)

    choice = models.CharField(
        null=True,
        max_length=2,
        choices=(('A', 'A'), ('B', 'B')),
        doc='either A or B',
    )

    def other_participant(self):
        """Returns other participant in match"""
        return self.other_participants_in_match()[0]

    def set_payoff(self):

        payoff_matrix = {
            'A': {
                'A': self.treatment.similar_amount,
                'B': self.treatment.dissimilar_amount,
            },
            'B': {
                'A': self.treatment.dissimilar_amount,
                'B': self.treatment.similar_amount,
            }
        }

        self.payoff = payoff_matrix[self.choice][self.other_participant().choice]


def treatments():

    return [
        Treatment.create(
            similar_amount = 10,
            dissimilar_amount = 0,
        )
    ]