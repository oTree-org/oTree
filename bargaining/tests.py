# -*- coding: utf-8 -*-
from __future__ import division
from . import views
from ._builtin import Bot
import random
from otree.common import Money, money_range
from .models import Constants

class PlayerBot(Bot):

    def play(self):

        # start
        self.submit(views.Introduction)
        self.submit(views.Question1, dict(
            training_amount_mine=1, training_amount_other=2))
        self.submit(views.Feedback1)

        # request
        self.submit(views.Request, {"request_amount": random.randrange(
            Constants.amount_shared)})

        # results
        self.submit(views.Results)
