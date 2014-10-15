# -*- coding: utf-8 -*-
from __future__ import division
from . import views
from ._builtin import Bot
import random
from otree.common import Money, money_range
from .models import Constants

class PlayerBot(Bot):

    def play(self):

        self.submit(views.Introduction)

        self.submit(views.QuestionOne, {
            'training_question_1': '5',
        })

        self.submit(views.FeedbackOne)

        self.submit(views.QuestionTwo, {
            'training_question_2': 'Time travel (opens in pop up window)',
        })

        self.submit(views.FeedbackTwo)

        self.submit(views.QuestionThree, {
            'training_question_3': 'Any of the above',
        })

        self.submit(views.FeedbackThree)

        self.submit(views.QuestionFour, {
            'training_question_4': 'All of the above',
        })

        self.submit(views.FeedbackFour)

        self.submit(views.QuestionFive, {
            'training_question_5': 'Time spent on each page',
        })

        self.submit(views.FeedbackFive)

        self.submit(views.FormsDemo, {
            'demo_field1': '1',
            'demo_field2': 'otree'
        })

        self.submit(views.Results)

        self.submit(views.Finish)