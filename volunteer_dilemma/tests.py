# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play(self):
        self.submit(views.Introduction)
        self.submit(views.Question1, dict(training_my_payoff=60))
        self.submit(views.Feedback1)
        self.submit(views.Decision, dict(volunteer=True))
        self.submit(views.Results)

    def validate_play(self):
        pass
