# -*- coding: utf-8 -*-
from ptree.db import models
import ptree.models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

doc="""
Minimal prisoner's dilemma game. Single treatment. The players are asked separately whether they want to cooperate or compete.
Their choices directly determine the payoffs.
"""

class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'prisoner_minimal'


class Treatment(ptree.models.BaseTreatment):
    subsession = models.ForeignKey(Subsession)

    betray_amount = models.PositiveIntegerField(
        doc="""amount a participant makes if he chooses 'Compete' and the other chooses 'Cooperate'"""
    )
    friends_amount = models.PositiveIntegerField(
        doc="""amount both participants make if both participants choose 'Cooperate'"""
    )
    betrayed_amount = models.PositiveIntegerField(
        doc="""amount a participant makes if he chooses 'Cooperate' and the other chooses 'Compete'"""
    )

    enemies_amount = models.PositiveIntegerField(
        doc="""amount both participants make if both participants choose 'Compete'"""
    )


class Match(ptree.models.BaseMatch):

    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)

    participants_per_match = 2


class Participant(ptree.models.BaseParticipant):

    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)

    decision = models.CharField(
        max_length=10, null=True, verbose_name='What is your decision?',
        choices=(('Cooperate', 'I will cooperate'), ('Compete', 'I will compete')),
        doc="""This participant's decision"""
    )

    def other_participant(self):
        return self.other_participants_in_match()[0]

    def set_payoff(self):
        payoff_matrix = {'Cooperate': {'Cooperate': self.treatment.friends_amount,
                                       'Compete': self.treatment.betrayed_amount},
                         'Compete':   {'Cooperate': self.treatment.betray_amount,
                                       'Compete': self.treatment.enemies_amount}}

        self.payoff = (payoff_matrix[self.decision]
                                    [self.other_participant().decision])


def treatments():
    return [Treatment.create(betray_amount=30,
                             friends_amount=20,
                             enemies_amount=10,
                             betrayed_amount=0)]
