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
        self.submit(views.Question1, dict(training_my_payoff=60))
        self.submit(views.Feedback1)
        self.submit(views.Decision, dict(volunteer=True))
        self.submit(views.Results)
        self.submit(views.FeedbackQ, dict(feedback=4))
