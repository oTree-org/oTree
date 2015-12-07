# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer

from otree import widgets
from otree.common import Currency as c, currency_range
import random
# </standard imports>

doc = """
This is a one-shot "Prisoner's Dilemma". Two players are asked separately
whether they want to cooperate or defect. Their choices directly determine the
payoffs.
"""

source_code = "https://github.com/oTree-org/oTree/tree/master/prisoner"


bibliography = ()


links = {
    "Wikipedia": {
        "Prisoner's Dilemma":
            "https://en.wikipedia.org/wiki/Prisoner%27s_dilemma"
    }
}


keywords = ("Prisoner's Dilemma",)


class Constants(BaseConstants):
    name_in_url = 'prisoner'
    players_per_group = 2
    num_rounds = 1

    #  Points made if player defects and the other cooperates""",
    defect_cooperate_amount = c(300)

    # Points made if both players cooperate
    cooperate_amount = c(200)
    cooperate_defect_amount = c(0)
    defect_amount = c(100)
    base_points = c(50)

    training_1_choices = [
        'Alice gets 300 points, Bob gets 0 points',
        'Alice gets 200 points, Bob gets 200 points',
        'Alice gets 0 points, Bob gets 300 points',
        'Alice gets 100 points, Bob gets 100 points'
    ]


    training_1_correct = training_1_choices[0]

class Subsession(BaseSubsession):

    pass


class Group(BaseGroup):
    pass

class Player(BasePlayer):

    training_question_1 = models.CharField(
        choices=Constants.training_1_choices,
        widget=widgets.RadioSelect(),
        #timeout_default=Constants.training_1_choices[1]
    )

    def is_training_question_1_correct(self):
        return self.training_question_1 == Constants.training_1_correct

    decision = models.CharField(
        choices=['Cooperate', 'Defect'],
        doc="""This player's decision""",
        widget=widgets.RadioSelect()
    )

    def other_player(self):
        return self.get_others_in_group()[0]

    def set_payoff(self):
        points_matrix = {'Cooperate': {'Cooperate': Constants.cooperate_amount,
                                       'Defect': Constants.cooperate_defect_amount},
                         'Defect':   {'Cooperate': Constants.defect_cooperate_amount,
                                      'Defect': Constants.defect_amount}}

        self.payoff = (points_matrix[self.decision]
                                           [self.other_player().decision])

