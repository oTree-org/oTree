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
        yield (views.Introduction)
        yield (views.Question1, {
            "training_question_1_win_pick": random.randint(0, 100),
            "training_question_1_my_payoff": random.randint(0, 100),
        })
        yield (views.Feedback1)

        # make your guess
        yield (views.Guess, {"guess_value": random.randint(0, 100)})

        yield (views.Results)

