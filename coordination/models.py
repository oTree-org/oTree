# -*- coding: utf-8 -*-
"""Documentation at https://github.com/oTree-org/otree/wiki"""


from otree.db import models
import otree.models


doc = """
In the coordination game, two players are required to choose either A or B. Payoff to the players
is determined by whether the choices match or not.
Source code <a href="https://github.com/oTree-org/oTree/tree/master/coordination" target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'coordination'


class Treatment(otree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    match_amount = models.MoneyField(
        default=1.00,
        doc="""Payoff for each player if choices match"""
    )

    mismatch_amount = models.MoneyField(
        default=0.00,
        doc="""Payoff for each player if choices don't match"""
    )


class Match(otree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_match = 2

    def set_payoffs(self):
        p1 = self.get_player_by_index(1)
        p2 = self.get_player_by_index(2)

        if p1.choice == p2.choice:
            p1.payoff = p2.payoff = self.treatment.match_amount
        else:
            p1.payoff = p2.payoff = self.treatment.mismatch_amount


class Player(otree.models.BasePlayer):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    choice = models.CharField(
        default=None,
        choices=['A', 'B'],
        doc="""Either A or B""",
    )

    def other_player(self):
        """Returns other player in match"""
        return self.other_players_in_match()[0]


def treatments():

    return [Treatment.create()]
