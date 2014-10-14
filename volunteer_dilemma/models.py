# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
from otree import widgets
from otree.common import Money, money_range
import random
# </standard imports>

doc = """
In the volunteer's dilemma game, players are asked separately whether or not they want to
volunteer. If at least one player volunteers, every player receives a general benefit/payoff.
The players who volunteer will, however, incur a given cost.
Source code <a href="https://github.com/oTree-org/oTree/tree/master/volunteer_dilemma" target="_blank">here</a>.
"""

class Constants:

    #"""Payoff for each player if at least one volunteers"""
    general_benefit = Money(1.00)\

    # """Cost incurred by volunteering player"""
    volunteer_cost = Money(0.40)


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'volunteer_dilemma'



class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_group = 3

    def set_payoffs(self):
        if any(p.volunteer for p in self.get_players()):
            baseline_amount = Constants.general_benefit
        else:
            baseline_amount = 0
        for p in self.get_players():
            p.payoff = baseline_amount
            if p.volunteer:
                p.payoff -= Constants.volunteer_cost


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    volunteer = models.NullBooleanField(
        doc="""Whether player volunteers""",
        widget=widgets.RadioSelect(),
    )


