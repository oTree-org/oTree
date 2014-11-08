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
        self.submit(views.Question1, {'training_question_1': 200})
        self.submit(views.Feedback1)

        # units to produce
        self.submit(views.Decide, {'units': random.choice(range(0, Constants.max_units_per_player + 1))})

        # results
        self.submit(views.Results)
