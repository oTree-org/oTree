# -*- coding: utf-8 -*-
from __future__ import division
"""Documentation at https://github.com/wickens/django-otree-docs/wiki"""

from otree.db import models
import otree.models
from otree.common import Money, money_range

author = 'Your name here'

doc = """
A quiz that asks the participants some questions, then tells them which answers were right and wrong.
Can be used for general quizzes, or for control/training questions prior to the experiment.
"""

class Subsession(otree.models.BaseSubsession):

    name_in_url = 'quiz'


class Treatment(otree.models.BaseTreatment):
    """Leave this class empty"""
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>


class Match(otree.models.BaseMatch):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    treatment = models.ForeignKey(Treatment)
    # </built-in>

    players_per_match = 1


class Player(otree.models.BasePlayer):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    treatment = models.ForeignKey(Treatment, null = True)
    match = models.ForeignKey(Match, null = True)
    # </built-in>

    q_doctor = models.PositiveIntegerField(
        default=None,
        verbose_name='''
        A doctor gives you 3 pills, and tells you to take 1 pill every 30 minutes starting right away.
        After how many minutes will you run out of pills?''',
        correct_answer=60,
        correct_answer_explanation='''
        You take the first pill right now, the second pill after 30 minutes, and the third pill after 60 minutes,
        so after 60 minutes you will have run out of pills.
        '''
    )

    q_meal = models.MoneyField(
        default=None,
        verbose_name='''
        A meal, including a beverage, costs {} in total.
        The food costs 5 times as much as the beverage.
        How much does the food cost?'
        '''.format(Money(1.20)),
        correct_answer=Money(1.00),
        correct_answer_explanation='''
        The beverage costs {} and the food costs {}
        '''.format(Money(0.20), Money(1.00))
    )


def treatments():
    return [Treatment.create()]