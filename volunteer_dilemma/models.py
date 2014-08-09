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


    volunteer_cost = models.MoneyField(
        null=True,
        doc="""
        Cost incurred by volunteering
        """)
    general_benefit = models.MoneyField(
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

    decision = models.CharField(
        null=True,
        max_length=10,
        choices=['Volunteer', 'Ignore'],
        doc="""
        Participant's decision to volunteer
        """
    )

    def other_participant(self):
        """Returns the opponent of the current player"""
        return self.other_participants_in_match()[0]

    def set_payoff(self):
        """Calculate participant payoff"""

        self.payoff = 0
        if self.decision == 'Volunteer' or self.other_participant().decision == 'Volunteer':
            self.payoff += self.treatment.general_benefit
        if self.decision == 'Volunteer':
            self.payoff -= self.treatment.volunteer_cost



def treatments():
    return [Treatment.create(
        volunteer_cost=0.40,
        general_benefit=1.00,
    )]