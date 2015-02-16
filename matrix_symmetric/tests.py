# -*- coding: utf-8 -*-
from __future__ import division
from . import views
from ._builtin import Bot
import random
from otree.common import Currency as c, currency_range
from .models import Constants

class PlayerBot(Bot):

    def play_round(self):

        # random decision
        choice = random.choice(['A', 'B'])
        self.submit(views.Decision, {"decision": choice})

        #  results
        self.submit(views.Results)

    def validate_play(self):
        pass
