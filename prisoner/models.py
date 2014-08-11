# -*- coding: utf-8 -*-
from ptree.db import models
import ptree.models


doc = """
Prisoner's dilemma game. Single treatment. Two players are asked separately whether they want to cooperate or Defect.
Their choices directly determine the payoffs.

<p>Source code <a href="https://github.com/wickens/ptree_library/tree/master/prisoner">here</a></p>
"""


class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'prisoner'


class Treatment(ptree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    betray_amount = models.MoneyField(
        doc="""amount a participant makes if he chooses 'Defect' and the other chooses 'Cooperate'""",
        default=0.30,
    )

    friend_amount = models.MoneyField(
        doc="""amount both participants make if both participants choose 'Cooperate'""",
        default=0.20,
    )
    betrayed_amount = models.MoneyField(
        doc="""amount a participant makes if he chooses 'Cooperate' and the other chooses 'Defect'""",
        default=0.10,
    )

    enemy_amount = models.MoneyField(
        doc="""amount both participants make if both participants choose 'Defect'""",
        default=0.00,
    )


class Match(ptree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    participants_per_match = 2


class Participant(ptree.models.BaseParticipant):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    decision = models.CharField(
        default=None, verbose_name='What is your decision?',
        choices=['Cooperate', 'Defect'],
        doc="""This participant's decision"""
    )

    def other_participant(self):
        """Returns other participant in match"""
        return self.other_participants_in_match()[0]

    def set_payoff(self):
        """Calculate participant payoff"""
        payoff_matrix = {'Cooperate': {'Cooperate': self.treatment.friend_amount,
                                       'Defect': self.treatment.betrayed_amount},
                         'Defect':   {'Cooperate': self.treatment.betray_amount,
                                       'Defect': self.treatment.enemy_amount}}

        self.payoff = (payoff_matrix[self.decision]
                                    [self.other_participant().decision])


def treatments():
    return [Treatment.create()]