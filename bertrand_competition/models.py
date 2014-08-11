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

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    minimum_price = models.MoneyField(
        default=0.20,
        doc="""
        The minimum price that can be set i.e equivalent to marginal cost.
        """
    )

    maximum_price = models.MoneyField(
        default=1.00,
        doc="""
        The maximum price that can be set .
        """
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

    price = models.MoneyField(
        default=None,
        doc="""
        The participant's target price
        """
    )

    is_winner = models.BooleanField(
        default=False,
        doc="""
        Whether this participant is the winner of the match
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
    return [Treatment.create()]