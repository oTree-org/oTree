# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):

        self.submit(views.Introduction)

        payoff = random.randint(
            Constants.min_allowable_bid, Constants.max_allowable_bid
        )
        self.submit(views.Question, {"training_question_1_my_payoff": payoff})
        self.submit(views.Feedback1)

        payoff = random.randint(
            Constants.min_allowable_bid, Constants.max_allowable_bid
        )
        self.submit(views.Bid, {"bid_amount": payoff})

        self.submit(views.Results)

    def validate_play(self):
        pass


