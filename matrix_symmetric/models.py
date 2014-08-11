# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-otree-docs/wiki"""

from otree.db import models
import otree.models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

doc = """
Matrix Symmetric is a game in which the identity of the player does not change the resulting game facing that player.
Each player earns the same payoff when making the same choice against similar choices of his competitors.

<p>Source code <a href="https://github.com/wickens/otree_library/tree/master/matrix_symmetric">here</a></p>
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'matrix_symmetric'


class Treatment(otree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    self_A_other_A = models.MoneyField(default=0.10)
    self_A_other_B = models.MoneyField(
        default=0.00,
        doc='''How much I make if I choose A and the other participant chooses B'''
    )
    self_B_other_A = models.MoneyField(default=0.30)
    self_B_other_B = models.MoneyField(default=0.40)


class Match(otree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    participants_per_match = 2


class Participant(otree.models.BaseParticipant):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    def other_participant(self):
        """Returns other participant in match"""
        return self.other_participants_in_match()[0]

    decision = models.CharField(
        default=None,
        choices=['A','B'],
        doc='either A or B',
    )

    def set_payoff(self):

        payoff_matrix = {
            'A': {
                'A': self.treatment.self_A_other_A,
                'B': self.treatment.self_A_other_B,
            },
            'B': {
                'A': self.treatment.self_B_other_A,
                'B': self.treatment.self_B_other_B,
            }
        }

        self.payoff = payoff_matrix[self.decision][self.other_participant().decision]


def treatments():
    return [Treatment.create()]