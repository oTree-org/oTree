# -*- coding: utf-8 -*-
from __future__ import division
import guessing.views as views
from guessing._builtin import Bot
import random


class PlayerBot(Bot):

    def play(self):

        # start game
        self.submit(views.Introduction)

        # make your guess
        self.submit(views.Guess, {"guess_value": random.randint(1, 100)})

        self.submit(views.Results)
