# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-ptree-docs/wiki"""

from ptree.db import models
import ptree.models


doc = """
Volunteer's Dilemma Game. Two participants are asked separately whether they want to
volunteer or ignore. Their choices directly determine the payoffs.

<p>Source code <a href="https://github.com/wickens/ptree_library/tree/master/volunteer_dilemma">here</a></p>
"""


class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'volunteer_dilemma'


class Treatment(ptree.models.BaseTreatment):
    subsession = models.ForeignKey(Subsession)


    volunteer_cost = models.PositiveIntegerField(
        null=True,
        doc="""
        Cost incurred by volunteering
        """)
    general_benefit = models.PositiveIntegerField(
        null=True,
        doc="""
        General benefit for all the participants, If at least one volunteers
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

    DECISION_CHOICES = (
        ('Volunteer', 'Volunteer'),
        ('Ignore', 'Ignore'),
    )

    decision = models.CharField(
        null=True,
        max_length=10,
        choices=DECISION_CHOICES,
        doc="""
        Participant's decision to volunteer
        """
    )

    def other_participant(self):
        """Returns the opponent of the current player"""
        return self.other_participants_in_match()[0]

    def set_payoff(self):
        """Calculate participant payoff"""

        payoff_matrix = {'Volunteer': {'Volunteer': (self.treatment.general_benefit - self.treatment.volunteer_cost),
                                       'Ignore': (self.treatment.general_benefit - self.treatment.volunteer_cost)},
                         'Ignore':   {'Volunteer': self.treatment.general_benefit,
                                       'Ignore': 0}}

        self.payoff = (payoff_matrix[self.decision]
                                    [self.other_participant().decision])


def treatments():
    return [Treatment.create(
        volunteer_cost=40,
        general_benefit=100,
    )]