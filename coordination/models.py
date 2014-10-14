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
In the coordination game, two players are required to choose either A or B. Payoff to the players
is determined by whether the choices group or not.
Source code <a href="https://github.com/oTree-org/oTree/tree/master/coordination" target="_blank">here</a>.
"""

class Constants:
    # Payoff for each player if choices group
    group_amount = Money(1.00)

    # Payoff for each player if choices don't group
    mismatch_amount = Money(0.00)


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'coordination'


class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_group = 2

    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)

        if p1.choice == p2.choice:
            p1.payoff = p2.payoff = Constants.group_amount
        else:
            p1.payoff = p2.payoff = Constants.mismatch_amount


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    choice = models.CharField(
        doc="""Either A or B""",
        widget = widgets.RadioSelect()
    )

    def choice_choices(self):
        return ['A', 'B']

    def other_player(self):
        """Returns other player in group"""
        return self.get_others_in_group()[0]


