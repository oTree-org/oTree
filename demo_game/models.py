# -*- coding: utf-8 -*-
"""Documentation at https://github.com/oTree-org/otree/wiki"""

from otree.db import models
import otree.models
from otree import forms


doc = """
<p>
A simple 1-player game demonstrating some of oTree’s basic capabilities,
as well as its interaction with some plugins.
</p>
Source code <a href="https://github.com/oTree-org/oTree/tree/master/demo_game" target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'demo_game'


class Treatment(otree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    training_1_correct = 3
    training_2_correct = "Time travel (opens in pop up window)"
    training_3_correct = "Any of the above"
    training_4_correct = "Any participants' input/choice"


class Match(otree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_match = 1


class Player(otree.models.BasePlayer):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    demo_field1 = models.CharField(
        default=None,
        choices=['0', '1', '2', 'do not know'],
        doc="""field With radiobutton input.""",
        widget=forms.RadioSelect(),
    )
    demo_field2 = models.CharField(
        default=None,
        max_length=5,
        doc="""
        field with text input
        """
    )

    QUESTION_2_CHOICES = ['Embed images', 'Dynamic visualizations using HighCharts', 'Time travel (opens in pop up window)', 'Embed video', 'Embed audio']
    QUESTION_3_CHOICES = ['Windows', 'Mac OS X', 'iOS', 'Android', 'Any of the above']
    QUESTION_4_CHOICES = ["Any participants' input/choice", "Time spent on each page", "Invalid attempts from participants", "Answers to understanding questions", "Questionnaire input"]

    training_question_1 = models.IntegerField(null=True, verbose_name='')
    training_question_2 = models.CharField(max_length=100, null=True, choices=QUESTION_2_CHOICES, verbose_name='', widget=forms.RadioSelect())
    training_question_3 = models.CharField(max_length=100, null=True, choices=QUESTION_3_CHOICES, verbose_name='', widget=forms.RadioSelect())
    training_question_4 = models.CharField(max_length=100, null=True, choices=QUESTION_4_CHOICES, verbose_name='', widget=forms.RadioSelect())

    # check correct answers
    def is_training_question_1_correct(self):
        return self.training_question_1 == self.treatment.training_1_correct

    def is_training_question_2_correct(self):
        return self.training_question_2 == self.treatment.training_2_correct

    def is_training_question_3_correct(self):
        return self.training_question_3 == self.treatment.training_3_correct

    def is_training_question_4_correct(self):
        return self.training_question_4 == self.treatment.training_4_correct

    def set_payoff(self):
        self.payoff = 0


def treatments():
    return [Treatment.create()]