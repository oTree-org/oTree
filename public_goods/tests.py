# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from ._builtin import Bot
from .models import Constants
from . import views


class PlayerBot(Bot):

    def play_round(self):
        self.submit(views.Introduction)
        self.submit(views.Question, {"question": 92})
        self.submit(views.Feedback)
        self.submit(
            views.Contribute, {
                "contribution": random.choice(
                    range(0, int(Constants.endowment)))
            }
        )
        self.submit(views.Results)

    def validate_play(self):
        pass
