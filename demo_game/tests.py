# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from ._builtin import Bot
from .models import Constants
from . import views


class PlayerBot(Bot):

    def play_round(self):

        self.submit(views.Introduction)

        self.submit(views.Question1, {
            'training_question_1': '5',
        })

        self.submit(views.Feedback1)

        self.submit(views.Question2, {
            'training_question_2': 'Time travel (opens in pop up window)',
        })

        self.submit(views.Feedback2)

        self.submit(views.Question3, {
            'training_question_3': 'Any of the above',
        })

        self.submit(views.Feedback3)

        self.submit(views.Question4, {
            'training_question_4': 'All of the above',
        })

        self.submit(views.Feedback4)

        self.submit(views.Question5, {
            'training_question_5': 'Time spent on each page',
        })

        self.submit(views.Feedback5)

        self.submit(views.FormsDemo, {
            'demo_field1': '1',
            'demo_field2': 'otree'
        })

        self.submit(views.Results)

        self.submit(views.Finish)

    def validate_play(self):
        pass
