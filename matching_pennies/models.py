# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-ptree-docs/wiki"""

from ptree.db import models
import ptree.models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

doc = """
Matching pennies is a two-player prediction game.
One player is known as the MARCHER, the other player is the MISMATCHER.
The MARCHER aims to see matching pennies.
The MISMATCHER wants the pennies not to match.
Both players simultaneously select either heads or tails.
If the pennies match then the MATCHER wins(both heads or tails), otherwise the MISMATCHER wins(one heads, one tails).
"""


class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'matching_pennies'


class Treatment(ptree.models.BaseTreatment):
    subsession = models.ForeignKey(Subsession)
    winner_amount = models.PositiveIntegerField(null=True,
                        doc="""
                        The amount to be won by either matcher or mismatcher
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

    # head/tail choice
    Head_Tail = (('head', 'Head'),
                ('tail', 'Tail'))
    penny_side = models.CharField(
        max_length=4,
        choices=Head_Tail,
        doc="""
        Player's decisions: Head or Tail
        """
    )

    def other_participant(self):
        return self.other_participants_in_match()[0]

    def set_payoff(self):
        payoff_matrix = {'head': {'head': 'Matcher',
                                       'tail': 'Mismatcher'},
                         'tail':   {'head': 'Mismatcher',
                                       'tail': 'Matcher'}}

        outcome = (payoff_matrix[self.penny_side]
                                    [self.other_participant().penny_side])
        if outcome == 'Matcher' and self.index_among_participants_in_match == 1:
            self.payoff = self.treatment.winner_amount
        elif outcome == 'Mismatcher' and self.index_among_participants_in_match == 2:
            self.payoff = self.treatment.winner_amount
        else:
            self.payoff = 0


def treatments():

    treatment_list = []

    treatment = Treatment(
        winner_amount=100,
    )

    treatment_list.append(treatment)

    return treatment_list