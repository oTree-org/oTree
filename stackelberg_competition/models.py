# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-ptree-docs/wiki"""

from ptree.db import models
import ptree.models


doc = """
<p>
    In Stackelberg Competition, participants play as firm owners(in duopoly market), each deciding sequentially on how
    much quantity to produce in order to make profit. The Participant to start is chosen randomly.
</p>
<p>
    Source code <a href="https://github.com/wickens/ptree_library/tree/master/stackelberg_competition">here</a>
</p>
"""


class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'stackelberg_competition'


class Treatment(ptree.models.BaseTreatment):
    subsession = models.ForeignKey(Subsession)

    total_capacity = models.PositiveIntegerField(
        null=True,
        doc="""
        Combined production capacity of both participants(firms)
        """
    )


class Match(ptree.models.BaseMatch):

    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)

    price = models.PositiveIntegerField(
        null=True,
        doc="""
        Price of goods: P=600-q1-q2
        """
        )

    participants_per_match = 2


class Participant(ptree.models.BaseParticipant):

    match = models.ForeignKey(Match, null = True)
    treatment = models.ForeignKey(Treatment, null = True)
    subsession = models.ForeignKey(Subsession)

    quantity = models.PositiveIntegerField(
        null=True,
        doc="""
        Quantity of goods to produce..
        """
    )

    def other_participant(self):
        """Returns the opponent of the current player"""
        return self.other_participants_in_match()[0]

    def set_payoff(self):
        self.match.price = self.treatment.total_capacity - self.quantity - self.other_participant().quantity
        self.payoff = self.match.price * self.quantity


def treatments():

    treatment_list = []

    treatment = Treatment(
        total_capacity=60,
    )

    treatment_list.append(treatment)

    return treatment_list