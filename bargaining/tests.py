# -*- coding: utf-8 -*-
from __future__ import division
import bargaining.views as views
from bargaining._builtin import Bot
import random


class PlayerBot(Bot):

    def play(self):

        # start
        self.submit(views.Introduction)
        self.submit(views.Question1, dict(
            training_amount_mine=1, training_amount_other=2))
        self.submit(views.Feedback1)

        # request
        self.submit(views.Request, {"request_amount": random.randrange(
            self.subsession.amount_shared)})

        # results
        self.submit(views.Results)
