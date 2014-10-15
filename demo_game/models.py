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
<p>
A simple 1-player game demonstrating some of oTree’s basic capabilities,
as well as its interaction with some plugins.
</p>
Source code <a href="https://github.com/oTree-org/oTree/tree/master/demo_game" target="_blank">here</a>.
"""

class Constants:
    training_1_correct = 5
    training_2_correct = "Time travel (opens in pop up window)"
    training_3_correct = "Any of the above"
    training_4_correct = "All of the above"
    training_5_correct = "Any participants' input/choice"

class Subsession(otree.models.BaseSubsession):

    name_in_url = 'demo_game'


class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_group = 1


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    demo_field1 = models.CharField(
        doc="""field With radiobutton input.""",
        widget=widgets.RadioSelect(),
    )
    demo_field2 = models.CharField(
        max_length=5,
        doc="""
        field with text input
        """
    )

    def demo_field1_choices(self):
        return ['0', '1', '2', 'do not know']

    training_question_1 = models.IntegerField(null=True, verbose_name='', widget=widgets.TextInput())
    training_question_2 = models.CharField(max_length=100, null=True, verbose_name='', widget=widgets.RadioSelect())
    training_question_3 = models.CharField(max_length=100, null=True, verbose_name='', widget=widgets.RadioSelect())
    training_question_4 = models.CharField(max_length=100, null=True, verbose_name='', widget=widgets.RadioSelect())
    training_question_5 = models.CharField(max_length=100, null=True, verbose_name='', widget=widgets.RadioSelect())

    def training_question_2_choices(self):
        return ['Embed images', 'Dynamic visualizations using HighCharts', 'Time travel (opens in pop up window)', 'Embed video', 'Embed audio']

    def training_question_3_choices(self):
        return ['Windows', 'Mac OS X', 'iOS', 'Android', 'Any of the above']

    def training_question_4_choices(self):
        return ["Calculation of payoff", "Progress of players through pages", "Values submitted by the players", "Whether players have visited the game", "All of the above"]

    def training_question_5_choices(self):
        return ["Any participants' input/choice", "Time spent on each page", "Invalid attempts from participants", "Answers to understanding questions", "Questionnaire input"]


    def training_question_1_error_message(self, value):
        if value < 0 and abs(value) % 2 == 0:
            return 'Your entry is invalid.'

    # check correct answers
    def is_training_question_1_correct(self):
        return self.training_question_1 == Constants.training_1_correct

    def is_training_question_2_correct(self):
        return self.training_question_2 == Constants.training_2_correct

    def is_training_question_3_correct(self):
        return self.training_question_3 == Constants.training_3_correct

    def is_training_question_4_correct(self):
        return self.training_question_4 == Constants.training_4_correct

    def is_training_question_5_correct(self):
        return self.training_question_5 == Constants.training_5_correct

    def set_payoff(self):
        self.payoff = 0


