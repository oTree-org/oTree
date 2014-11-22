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

        self.submit(views.Question1, {'training_question_1': 20})
        self.submit(views.Feedback1)

        # player one
        if self.player.id_in_group == 1:
            quantity = random.randint(0, Constants.max_units_per_player)
            self.submit(views.ChoiceOne, {'quantity': quantity})

        # player two
        elif self.player.id_in_group == 2:
            quantity = random.randint(0, Constants.max_units_per_player)
            self.submit(views.ChoiceTwo, {'quantity': quantity})

        self.submit(views.Results)

    def validate_play(self):
        pass


