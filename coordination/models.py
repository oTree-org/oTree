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

    match_amount = models.MoneyField(
        null=True,
        doc="""
        amount each participant is rewarded for having match choices
        """
    )

    mismatch_amount = models.MoneyField(
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
        choices=['A', 'B'],
        doc='either A or B',
    )

    def other_participant(self):
        """Returns other participant in match"""
        return self.other_participants_in_match()[0]

    def set_payoff(self):

        if self.choice == self.other_participant().choice:
            return self.treatment.match_amount
        return self.treatment.mismatch_amount


def treatments():

    return [
        Treatment.create(
            match_amount = 10,
            mismatch_amount = 0,
        )
    ]