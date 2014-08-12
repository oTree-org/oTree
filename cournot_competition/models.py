# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-otree-docs/wiki"""

from otree.db import models
import otree.models


doc = """
<p>
In Cournot Competition, players play as firm owners(in duopoly market), each deciding simultaneously on
how much quantity to produce in order to make a profit. Players decide on choosing to maximise their profits or
cooperating with others to improve profits.
</p>
<p>
Source code <a href="https://github.com/oTree-org/oTree/tree/master/cournot_competition">here</a>.
</p>
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'cournot_competition'


class Treatment(otree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    total_capacity = models.PositiveIntegerField(
        default=60,
        doc="""
        Combined production capacity of both players(firms)
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

    players_per_match = 2


class Player(otree.models.BasePlayer):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>


    quantity = models.PositiveIntegerField(
        default=None,
        doc="""
        Quantity of goods to produce.
        """
    )

    def other_player(self):
        """Returns the opponent of the current player"""
        return self.other_players_in_match()[0]

    def set_payoff(self):
        #FIXME: should quantity be a MoneyField?
        self.match.price = self.treatment.total_capacity - self.quantity - self.other_player().quantity
        self.payoff = self.match.price * self.quantity


def treatments():
    return [Treatment.create()]