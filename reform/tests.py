# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    """Bot that plays one round"""

    def play_round(self):

        if round == Constants.num_rounds:
            self.submit(views.Decisions, {'approval': random.randint(0,1), 'abolish': 0})
            self.submit(views.FinalResults)
        else:
            self.submit(views.Decisions, {'approval': 1, 'abolish': 0})

    def validate_play(self):
        pass
