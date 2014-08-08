# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-ptree-docs/wiki"""

from ptree.db import models
import ptree.models


doc = """
Stag Hunt
"""


class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'stag_hunt'


class Treatment(ptree.models.BaseTreatment):
    subsession = models.ForeignKey(Subsession)

    stag_stag_amount = models.MoneyField(
        null=True,
        doc="""
        Amount rewarded for choosing both stag
        """
    )
    stag_hare_amount = models.MoneyField(
        null=True,
        doc="""
        Amount rewarded for choosing stag and hare
        """
    )
    hare_stag_amount = models.MoneyField(
        null=True,
        doc="""
        Amount rewarded for choosing hare and stag
        """
    )
    hare_hare_amount = models.MoneyField(
        null=True,
        doc="""
        Amount rewarded for choosing both hare
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
        max_length=5,
        choices=['Stag', 'Hare'],
        doc='either Stag or Hare',
    )

    def other_participant(self):
        """Returns other participant in match"""
        return self.other_participants_in_match()[0]

    def set_payoff(self):

        payoff_matrix = {
            'Stag': {
                'Stag': self.treatment.stag_stag_amount,
                'Hare': self.treatment.stag_hare_amount,
            },
            'Hare': {
                'Stag': self.treatment.hare_stag_amount,
                'Hare': self.treatment.hare_hare_amount,
            }
        }
        self.payoff = payoff_matrix[self.decision][self.other_participant().decision]


def treatments():
    return [
        Treatment.create(
            stag_stag_amount=0.20,
            stag_hare_amount=0.00,
            hare_stag_amount=0.10,
            hare_hare_amount=0.10)
    ]