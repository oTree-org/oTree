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
            "training_question_1_husband": random.randint(0, 100),
            "training_question_1_wife": random.randint(0, 100),
        })
        self.submit(views.FeedbackOne)

        self.submit(views.Decide, {
            "decision": random.choice(['Football', 'Opera'])
        })

        # results
        self.submit(views.Results)
