# -*- coding: utf-8 -*-
from __future__ import division
"""Documentation at https://github.com/oTree-org/otree/wiki"""

from otree.db import models
import otree.models
from otree import widgets


doc = """
In the volunteer's dilemma game, players are asked separately whether or not they want to
volunteer. If at least one player volunteers, every player receives a general benefit/payoff.
The players who volunteer will, however, incur a given cost.
Source code <a href="https://github.com/oTree-org/oTree/tree/master/volunteer_dilemma" target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'volunteer_dilemma'

    general_benefit = models.MoneyField(
        default=1.00,
        doc="""Payoff for each player if at least one volunteers"""
    )

    volunteer_cost = models.MoneyField(
        default=0.40,
        doc="""Cost incurred by volunteering player"""
    )


class Treatment(otree.models.BaseTreatment):
    """Leave this class empty"""

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>



class Match(otree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_match = 3

    def set_payoffs(self):
        if any(p.volunteer for p in self.players):
            baseline_amount = self.subsession.general_benefit
        else:
            baseline_amount = 0
        for p in self.players:
            p.payoff = baseline_amount
            if p.volunteer:
                p.payoff -= self.subsession.volunteer_cost


class Player(otree.models.BasePlayer):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    volunteer = models.NullBooleanField(
        default=None,
        doc="""Whether player volunteers""",
        widget=widgets.RadioSelect(),
    )


def treatments():

    return [Treatment.create()]
