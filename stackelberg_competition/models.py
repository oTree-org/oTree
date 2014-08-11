# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-otree-docs/wiki"""

from otree.db import models
import otree.models


doc = """
<p>
    In Stackelberg Competition, participants play as firm owners(in duopoly market), each deciding sequentially on how
    much quantity to produce in order to make profit. The Participant to start is chosen randomly.
</p>
<p>
    Source code <a href="https://github.com/wickens/otree_library/tree/master/stackelberg_competition">here</a>
</p>
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'stackelberg_competition'


class Treatment(otree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    total_capacity = models.PositiveIntegerField(
        default=60,
        doc="""
        Combined production capacity of both participants(firms)
        """
    )


class Match(otree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    price = models.MoneyField(
        default=None,
        doc="""
        Price of goods: P=600-q1-q2
        """
        )

    participants_per_match = 2


class Participant(otree.models.BaseParticipant):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    quantity = models.PositiveIntegerField(
        default=None,
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
    return [Treatment.create()]