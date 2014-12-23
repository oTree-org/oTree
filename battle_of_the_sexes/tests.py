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
        self.submit(views.Question1, {
            "training_question_1_husband": random.randint(0, 100),
            "training_question_1_wife": random.randint(0, 100),
        })
        self.submit(views.Feedback1)

        self.submit(
            views.Decide, {"decision": random.choice(['Football', 'Opera'])}
        )

        # results
        self.submit(views.Results)

    def validate_play(self):
        pass
