# -*- coding: utf-8 -*-
"""Documentation at https://github.com/oTree-org/otree/wiki"""

from otree.db import models
import otree.models

PLAYERS_PER_MATCH = 3

doc = """
Volunteer's Dilemma Game. {} players are asked separately whether they want to
volunteer or ignore. If at least one person volunteers, everybody receives a general benefit.
But each person who volunteers incurs a cost.

Source code <a href="https://github.com/oTree-org/oTree/tree/master/volunteer_dilemma" target="_blank">here</a>.
""".format(PLAYERS_PER_MATCH)


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
        General benefit for all the players, if at least one volunteers
        """
    )


class Match(otree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_match = PLAYERS_PER_MATCH

    def set_payoffs(self):
        """Calculate player payoff"""

        someone_volunteered = any(p.decision == 'Volunteer' for p in self.players)
        if someone_volunteered:
            baseline_amount = self.treatment.general_benefit
        else:
            baseline_amount = 0
        for p in self.players:
            p.payoff = baseline_amount
            if p.decision == 'Volunteer':
                p.payoff -= self.treatment.volunteer_cost


class Player(otree.models.BasePlayer):


    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>


    decision = models.CharField(
        default=None,
        choices=['Volunteer', 'Ignore'],
        doc="""
        Player's decision to volunteer
        """
    )

def treatments():
    return [Treatment.create()]