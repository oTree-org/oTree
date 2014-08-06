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

    football_husband_amount = models.MoneyField(
        null=True,
        doc="""
        Amount rewarded to husband if football is chosen
        """
    )
    football_wife_amount = models.MoneyField(
        null=True,
        doc="""
        Amount rewarded to wife if football is chosen
        """
    )
    mismatch_amount = models.MoneyField(
        null=True,
        doc="""
        Amount rewarded for choosing football and opera for either participants
        """
    )
    opera_husband_amount = models.MoneyField(
        null=True,
        doc="""
        Amount rewarded to husband if opera is chosen
        """
    )
    opera_wife_amount = models.MoneyField(
        null=True,
        doc="""
        Amount rewarded to wife if opera is chosen
        """
    )


class Match(ptree.models.BaseMatch):

    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)

    participants_per_match = 2


    def set_payoffs(self):
        husband = self.get_participant('husband')
        wife = self.get_participant('wife')

        if husband.decision != wife.decision:
            husband.payoff = self.treatment.mismatch_amount
            wife.payoff = self.treatment.mismatch_amount

        else:
            if husband.decision == 'football':
                husband.payoff = self.treatment.football_husband_amount
                wife.payoff = self.treatment.football_wife_amount
            else:
                husband.payoff = self.treatment.opera_husband_amount
                wife.payoff = self.treatment.opera_wife_amount

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

    def role(self):
        roles = {
            1: 'husband',  # football preference
            2: 'wife'  # opera preference
        }

        return roles[self.index_among_participants_in_match]


def treatments():
    return [
        Treatment.create(
            football_husband_amount=0.3,
            football_wife_amount=0.2,
            mismatch_amount=0,
            opera_husband_amount=0.2,
            opera_wife_amount=0.3
        )
    ]