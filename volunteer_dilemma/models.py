# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-otree-docs/wiki"""

from otree.db import models
import otree.models


doc = """
Volunteer's Dilemma Game. Two players are asked separately whether they want to
volunteer or ignore. Their choices directly determine the payoffs.

Source code <a href="https://github.com/oTree-org/oTree/tree/master/volunteer_dilemma" target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'volunteer_dilemma'


class Treatment(otree.models.BaseTreatment):
    subsession = models.ForeignKey(Subsession)


    volunteer_cost = models.MoneyField(
        default=0.40,
        doc="""
        Cost incurred by volunteering
        """)

    general_benefit = models.MoneyField(
        default=1.00,
        doc="""
        General benefit for all the players, If at least one volunteers
        """
    )


class Match(otree.models.BaseMatch):

    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)

    players_per_match = 2


class Player(otree.models.BasePlayer):

    # <built-in>
    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>
    # </built-in>

    decision = models.CharField(
        default=None,
        choices=['Volunteer', 'Ignore'],
        doc="""
        Player's decision to volunteer
        """
    )

    def other_player(self):
        """Returns the opponent of the current player"""
        return self.other_players_in_match()[0]

    def set_payoff(self):
        """Calculate player payoff"""

        self.payoff = 0
        if self.decision == 'Volunteer' or self.other_player().decision == 'Volunteer':
            self.payoff += self.treatment.general_benefit
        if self.decision == 'Volunteer':
            self.payoff -= self.treatment.volunteer_cost



def treatments():
    return [Treatment.create()]