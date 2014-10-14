# -*- coding: utf-8 -*-
from __future__ import division
from . import views
from ._builtin import Bot
import random
from otree.common import Money, money_range
from .models import Constants

class PlayerBot(Bot):

    def play(self):

        self.submit(views.Introduction)

        self.submit(views.QuestionOne, {'training_question_1': 20})
        self.submit(views.FeedbackOne)

        # player one
        if self.player.id_in_group == 1:
            self.play_1()

        # player two
        elif self.player.id_in_group == 2:
            self.play_2()

        self.submit(views.Results)

    def play_1(self):
        self.submit(views.ChoiceOne, {'quantity': random.randint(0, Constants.max_units_per_player)})

    def play_2(self):
        self.submit(views.ChoiceTwo, {'quantity': random.randint(0, Constants.max_units_per_player)})

