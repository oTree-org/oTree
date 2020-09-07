# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):

        yield (views.Introduction)

        yield (views.Question, {'training_question_1': 20})
        yield (views.Feedback)

        # player one
        if self.player.id_in_group == 1:
            quantity = random.randint(0, Constants.max_units_per_player)
            yield (views.ChoiceOne, {'quantity': quantity})

        # player two
        elif self.player.id_in_group == 2:
            quantity = random.randint(0, Constants.max_units_per_player)
            yield (views.ChoiceTwo, {'quantity': quantity})

        yield (views.Results)



