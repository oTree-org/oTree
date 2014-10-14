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

        self.submit(views.QuestionOne, {'training_question_1': 'Alice gets 300 points, Bob gets 0 points'})

        self.submit(views.FeedbackOne)

        self.submit(views.Decision, {"decision": random.choice(['Cooperate', 'Defect'])})

        self.submit(views.Results)
