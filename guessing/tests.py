# -*- coding: utf-8 -*-
from __future__ import division
from . import views
from ._builtin import Bot
import random
from otree.common import Money, money_range
from .models import Constants

class PlayerBot(Bot):

    def play(self):

        # start game
        self.submit(views.Introduction)

        # make your guess
        self.submit(views.Guess, {"guess_value": random.randint(0, 100)})

        self.submit(views.Results)
