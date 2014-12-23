# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from ._builtin import Bot
from .models import Constants
from . import views


class PlayerBot(Bot):

    def play_round(self):
        self.submit(
            views.Feedback,
            {'feedback': random.choice(Constants.feedback_choices)}
        )

    def validate_play(self):
        pass
