# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-ptree-docs/wiki"""

from ptree.db import models
import ptree.models


doc = """
Battle of the sexes.
"""


class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'battle_of_the_sexes'


class Treatment(ptree.models.BaseTreatment):
    subsession = models.ForeignKey(Subsession)

    football_husband_amount = models.PositiveIntegerField(
        null=True,
        doc="""
        Amount rewarded to p1 for choosing football
        """
    )
    football_wife_amount = models.PositiveIntegerField(
        null=True,
        doc="""
        Amount rewarded to p2 for choosing football
        """
    )
    football_opera_amount = models.PositiveIntegerField(
        null=True,
        doc="""
        Amount rewarded for choosing football and opera for either participants
        """
    )
    opera_husband_amount = models.PositiveIntegerField(
        null=True,
        doc="""
        Amount rewarded to p1 for choosing both opera
        """
    )
    opera_wife_amount = models.PositiveIntegerField(
        null=True,
        doc="""
        Amount rewarded to p1 for choosing both opera
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
        choices=['football', 'opera'],
        doc='either football or opera',
    )

    def other_participant(self):
        """Returns other participant in match"""
        return self.other_participants_in_match()[0]

    def set_payoff(self):
        if self.role() == 'husband':
            payoff_matrix = {
                'football': {
                    'football': self.treatment.football_husband_amount,
                    'opera': self.treatment.football_opera_amount,
                },
                'opera': {
                    'football': self.treatment.football_opera_amount,
                    'opera': self.treatment.opera_husband_amount,
                }
            }
        else:
            payoff_matrix = {
                'football': {
                    'football': self.treatment.football_wife_amount,
                    'opera': self.treatment.football_opera_amount,
                },
                'opera': {
                    'football': self.treatment.football_opera_amount,
                    'opera': self.treatment.opera_wife_amount,
                }
            }
        self.payoff = payoff_matrix[self.decision][self.other_participant().decision]

    def role(self):
        roles = {
            1: 'husband',  # football preference
            2: 'wife'  # opera preference
        }

        return roles[self.index_among_participants_in_match]


def treatments():
    return [
        Treatment.create(
            football_husband_amount=30,
            football_wife_amount=20,
            football_opera_amount=0,
            opera_husband_amount=20,
            opera_wife_amount=30
        )
    ]