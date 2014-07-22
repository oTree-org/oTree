# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-ptree-docs/wiki"""

from ptree.db import models
import ptree.models


doc = """
In Bertrand Competition, participants play as firm owners(in duopoly market), each deciding simultaneously on how
much price to set for their products. The participant with the lowest price carries the day and becomes the winner.

<p>Source code <a href="https://github.com/wickens/ptree_library/tree/master/bertrand_competition">here</a></p>
"""


class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'bertrand_competition'


class Treatment(ptree.models.BaseTreatment):
    subsession = models.ForeignKey(Subsession)

    minimum_price = models.PositiveIntegerField(
        null=True,
        doc="""
        The minimum price that can be set i.e equivalent to marginal cost.
        """
    )

    maximum_price = models.PositiveIntegerField(
        null=True,
        doc="""
        The maximum price that can be set .
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

    price = models.PositiveIntegerField(
        null=True,
        doc="""
        Target price by a given participant.
        """
    )

    is_winner = models.BooleanField(
        default=False,
        doc="""
        Shows the winner in the competition.
        """
    )

    def other_participant(self):
        '''get the opponent participant'''
        return self.other_participants_in_match()[0]

    def set_payoff(self):
        if self.price < self.other_participant().price:
            self.is_winner = True
            self.payoff = self.price - self.treatment.minimum_price
        elif self.price > self.other_participant().price:
            self.payoff = 0
        elif self.price == self.other_participant().price:
            self.payoff = (self.price - self.treatment.minimum_price) / 2.0


def treatments():

    treatment_list = []

    treatment = Treatment(
        minimum_price=20,
        maximum_price=100,
    )

    treatment_list.append(treatment)

    return treatment_list