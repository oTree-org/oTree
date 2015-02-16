# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):

        # start game
        self.submit(views.Introduction)
        self.submit(views.Question1, {
            'training_answer_mine': 1, 'training_answer_others':2})
        self.submit(views.Feedback)

        claim = random.randrange(Constants.min_amount, Constants.max_amount)
        self.submit(views.Claim, {"claim": claim})

        self.submit(views.Results)

    def validate_play(self):
        pass
