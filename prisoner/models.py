# -*- coding: utf-8 -*-
from __future__ import division
from otree.db import models
import otree.models
from otree import widgets


doc = """
<p>This is a one-shot "Prisoner's Dilemma". Two players are asked separately whether they want to cooperate or defect.
Their choices directly determine the payoffs.</p>
<p>Source code <a href="https://github.com/oTree-org/oTree/tree/master/prisoner" target="_blank">here</a>.</p>
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'prisoner'

    betray_amount = models.PositiveIntegerField(
        doc="""Points made if player defects and the other cooperates""",
        default=300,
        )

    friend_amount = models.PositiveIntegerField(
        doc="""Points made if both players cooperate""",
        default=200,
        )
    betrayed_amount = models.PositiveIntegerField(
        doc="""Points made if player cooperates and the other defects""",
        default=100,
        )

    enemy_amount = models.PositiveIntegerField(
        doc="""Points made if both players defect""",
        default=0,
        )


class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_group = 2


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    points_earned = models.PositiveIntegerField(
        default=0,
        doc="""Points earned"""
    )

    decision = models.CharField(
        default=None,
        doc="""This player's decision""",
        widget=widgets.RadioSelect()
    )

    def decision_choices(self):
        return ['Cooperate', 'Defect']

    def other_player(self):
        return self.other_players_in_group()[0]

    def set_points(self):
        points_matrix = {'Cooperate': {'Cooperate': self.subsession.friend_amount,
                                       'Defect': self.subsession.betrayed_amount},
                         'Defect':   {'Cooperate': self.subsession.betray_amount,
                                      'Defect': self.subsession.enemy_amount}}

        self.points_earned = (points_matrix[self.decision]
                                           [self.other_player().decision])
2