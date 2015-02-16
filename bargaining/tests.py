# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):

        # start
        self.submit(views.Introduction)
        self.submit(
            views.Question1,
            {"training_amount_mine": 1, "training_amount_other": 2}
        )
        self.submit(views.Feedback)

        # request
        amount = random.randrange(Constants.amount_shared)
        self.submit(views.Request, {"request_amount": amount})

        # results
        self.submit(views.Results)

    def validate_play(self):
        pass
