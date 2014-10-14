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
<p>This is a one-shot "Prisoner's Dilemma". Two players are asked separately whether they want to cooperate or defect.
Their choices directly determine the payoffs.</p>
<p>Source code <a href="https://github.com/oTree-org/oTree/tree/master/prisoner" target="_blank">here</a>.</p>
"""

class Constants:

    #  Points made if player defects and the other cooperates""",
    defect_cooperate_amount = 300

    # Points made if both players cooperate
    cooperate_amount = 200
    cooperate_defect_amount = 0
    defect_amount = 100
    base_points = 50


    training_1_correct = "Alice gets 300 points, Bob gets 0 points"

class Subsession(otree.models.BaseSubsession):

    name_in_url = 'prisoner'





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

    training_question_1 = models.CharField(max_length=100, null=True, verbose_name='', widget=widgets.RadioSelect())

    def training_question_1_choices(self):
        return ['Alice gets 300 points, Bob gets 0 points',
                'Alice gets 200 points, Bob gets 200 points',
                'Alice gets 0 points, Bob gets 300 points',
                'Alice gets 100 points, Bob gets 100 points']

    def is_training_question_1_correct(self):
        return self.training_question_1 == Constants.training_1_correct

    points_earned = models.PositiveIntegerField(
        default=0,
        doc="""Points earned"""
    )

    decision = models.CharField(
        doc="""This player's decision""",
        widget=widgets.RadioSelect()
    )

    def decision_choices(self):
        return ['Cooperate', 'Defect']

    def other_player(self):
        return self.get_others_in_group()[0]

    def set_points(self):
        points_matrix = {'Cooperate': {'Cooperate': Constants.cooperate_amount,
                                       'Defect': Constants.cooperate_defect_amount},
                         'Defect':   {'Cooperate': Constants.defect_cooperate_amount,
                                      'Defect': Constants.defect_amount}}

        self.points_earned = (points_matrix[self.decision]
                                           [self.other_player().decision])

    def set_payoff(self):
        self.payoff = 0

