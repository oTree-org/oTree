# -*- coding: utf-8 -*-
from __future__ import division
from . import views
from ._builtin import Bot
import random
from otree.common import Money, money_range
from .models import Constants
class PlayerBot(Bot):

    def play(self):

        # start game
        self.submit(views.Introduction)
        self.submit(views.Question1, dict(
            training_answer_mine=1, training_answer_others=2))
        self.submit(views.Feedback1)

        self.submit(views.Claim, {"claim": random.randrange(Constants.min_amount, Constants.max_amount)})


        self.submit(views.Results)
        self.submit(views.Question2, dict(feedback=3))