# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-otree-docs/wiki"""

from otree.db import models
import otree.models


doc = """
In Coordination game, There are two players which are required to choose either A or B.
If both Players chooses the same choice then they both wins, otherwise they loose.

<p>Source code <a href="https://github.com/wickens/otree_library/tree/master/coordination">here</a></p>
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'coordination'


class Treatment(otree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    match_amount = models.MoneyField(
        default=1.00,
        doc="""
        amount each player is rewarded for having match choices
        """
    )

    mismatch_amount = models.MoneyField(
        default=0.00,
        doc="""
        amount each player is rewarded for having different choices
        """
    )


class Match(otree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_match = 2


class Player(otree.models.BasePlayer):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    choice = models.CharField(
        default=None,
        choices=['A', 'B'],
        doc='either A or B',
    )

    def other_player(self):
        """Returns other player in match"""
        return self.other_players_in_match()[0]

    def set_payoff(self):

        if self.choice == self.other_player().choice:
            self.payoff = self.treatment.match_amount
        else:
            self.payoff = self.treatment.mismatch_amount


def treatments():
    return [Treatment.create()]