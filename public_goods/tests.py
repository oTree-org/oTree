# -*- coding: utf-8 -*-
from __future__ import division
import public_goods.views as views
from public_goods._builtin import Bot
import random


class PlayerBot(Bot):

    def play(self):

        self.submit(views.Introduction)

        self.submit(views.Question, {"question": 92})

        self.submit(views.Feedback)

        self.submit(views.Contribute, {"contribution": random.choice(range(0, self.subsession.endowment))})

        self.submit(views.Results)

        self.submit(views.FeedbackQ, {"feedbackq": "Very well"})