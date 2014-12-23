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
        self.submit(views.Question1, {'training_question_1': 200})
        self.submit(views.Feedback1)

        # units to produce
        units = random.choice(range(0, Constants.max_units_per_player + 1))
        self.submit(views.Decide, {'units': units})

        # results
        self.submit(views.Results)

    def validate_play(self):
        pass
