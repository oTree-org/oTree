# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-ptree-docs/wiki"""

from ptree.db import models
import ptree.models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

doc = """
Matching pennies. Single treatment. Two players are given a penny each, and will at the same time choose either heads or tails.
One player wants the outcome to match; the other wants the outcome not to match.
If the outcomes match, the former player gets both pennies; if the outcomes do not match, the latter player gets both pennies.
"""


class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'matching_pennies'


class Treatment(ptree.models.BaseTreatment):

    subsession = models.ForeignKey(Subsession)

    initial_amount = models.PositiveIntegerField(
        null=True,
        doc="""The value of the pennies given to each player"""
    )


class Match(ptree.models.BaseMatch):

    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)

    participants_per_match = 2


class Participant(ptree.models.BaseParticipant):

    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)

    PENNY_CHOICES = (('heads', 'Heads'),
                     ('tails', 'Tails'))

    penny_side = models.CharField(
        max_length=5,
        choices=PENNY_CHOICES,
        doc="""Heads or tails"""
    )

    def other_participant(self):
        """Returns the opponent of the current player"""
        return self.other_participants_in_match()[0]

    def set_payoff(self):
        """Calculates payoffs"""
        payoff_matrix = {'heads': {'heads': 'match',
                                   'tails': 'mismatch'},
                         'tails':   {'heads': 'mismatch',
                                     'tails': 'match'}}

        outcome = (payoff_matrix[self.penny_side]
                                [self.other_participant().penny_side])

        if outcome == 'match' and self.index_among_participants_in_match == 1:
            self.payoff = self.treatment.initial_amount * 2
        elif outcome == 'mismatch' and self.index_among_participants_in_match == 2:
            self.payoff = self.treatment.initial_amount * 2
        else:
            self.payoff = 0


def treatments():

    treatment_list = []

    treatment = Treatment(
        initial_amount=100,
    )

    treatment_list.append(treatment)

    return treatment_list
