# -*- coding: utf-8 -*-
from __future__ import division
from . import views
from ._builtin import Bot
import random
from otree.common import Money, money_range
from .models import Constants

class PlayerBot(Bot):

    def play(self):

        # introduction
        self.submit(views.Introduction)

        # decision
        self.submit(views.Decision, {"decision": random.choice(['cooperate', 'defect'])})

        # results
        self.submit(views.Results)
