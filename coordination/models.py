# -*- coding: utf-8 -*-
from __future__ import division
"""Documentation at https://github.com/oTree-org/otree/wiki"""


from otree.db import models
import otree.models
from otree import widgets


doc = """
In the coordination game, two players are required to choose either A or B. Payoff to the players
is determined by whether the choices group or not.
Source code <a href="https://github.com/oTree-org/oTree/tree/master/coordination" target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'coordination'

    group_amount = models.MoneyField(
        default=1.00,
        doc="""Payoff for each player if choices group"""
    )

    mismatch_amount = models.MoneyField(
        default=0.00,
        doc="""Payoff for each player if choices don't group"""
    )




class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_group = 2

    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)

        if p1.choice == p2.choice:
            p1.payoff = p2.payoff = self.subsession.group_amount
        else:
            p1.payoff = p2.payoff = self.subsession.mismatch_amount


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    choice = models.CharField(
        default=None,
        doc="""Either A or B""",
        widget = widgets.RadioSelect()
    )

    def choice_choices(self):
        return ['A', 'B']

    def other_player(self):
        """Returns other player in group"""
        return self.other_players_in_group()[0]


