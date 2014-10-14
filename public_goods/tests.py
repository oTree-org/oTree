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

        self.submit(views.Question, {"question": 92})

        self.submit(views.Feedback)

        self.submit(views.Contribute, {"contribution": random.choice(range(0, Constants.endowment))})

        self.submit(views.Results)

        self.submit(views.FeedbackQ, {"feedbackq": "Very well"})