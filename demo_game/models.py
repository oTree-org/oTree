# -*- coding: utf-8 -*-
"""Documentation at https://github.com/oTree-org/otree/wiki"""

from otree.db import models
import otree.models


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

    training_1_correct = 2
    training_2_correct = 'Time travel (opens in pop up window)'


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
        choices=['yes', 'no'],
        doc="""
        field With radiobutton input.
        """
    )
    demo_field2 = models.TextField(
        default=None,
        doc="""
        field with textarea input
        """
    )
    demo_field3 = models.CharField(
        default=None,
        doc="""
        field with text input
        """
    )
    demo_field4 = models.CharField(
        default=None,
        choices=['accept', 'reject'],
        doc="""
        field with select choices input
        """
    )
    demo_field5 = models.PositiveIntegerField(
        default=None,
        doc="""
        field with positive integers and only odd numbers - see form validation
        """
    )

    QUESTION_2_CHOICES = ['Embed images', 'Dynamic visualizations using HighCharts', 'Time travel (opens in pop up window)', 'Embed video', 'Embed audio']

    training_question_1 = models.PositiveIntegerField(null=True, verbose_name=' ')
    training_question_2 = models.CharField(max_length=100, null=True, choices=QUESTION_2_CHOICES, verbose_name=' ')

    # check correct answers
    def is_training_question_1_correct(self):
        return self.training_question_1 == self.treatment.training_1_correct

    def is_training_question_2_correct(self):
        return self.training_question_2 == self.treatment.training_2_correct

    def set_payoff(self):
        self.payoff = 0


def treatments():
    return [Treatment.create()]