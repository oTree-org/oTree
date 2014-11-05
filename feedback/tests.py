# -*- coding: utf-8 -*-
from __future__ import division
from . import views
from ._builtin import Bot
import random
from otree.common import Currency, currency_range
from .models import Constants


class PlayerBot(Bot):

    def play(self):

        self.submit(
            views.Feedback,
            {'feedback': random.choice(Constants.feedback_choices)}
        )