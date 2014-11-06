# -*- coding: utf-8 -*-
from __future__ import division
from . import views
from ._builtin import Bot
import random
from otree.common import Currency as c, currency_range
from .models import Constants

class PlayerBot(Bot):

    def play(self):

        self.submit(views.Introduction)

        self.submit(views.QuestionOne, {
            "training_question_1_my_payoff": random.randint(
                Constants.min_allowable_bid, Constants.max_allowable_bid
            )
        })
        self.submit(views.FeedbackOne)

        self.submit(views.Bid, {
            "bid_amount": random.randint(
                Constants.min_allowable_bid, Constants.max_allowable_bid
            )
        })

        self.submit(views.Results)


