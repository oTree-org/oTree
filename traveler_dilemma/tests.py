# -*- coding: utf-8 -*-
from __future__ import division
from . import views
from ._builtin import Bot
import random
from otree.common import Money, money_range
from .models import Constants
class PlayerBot(Bot):

    def play(self):

        # basic assertions
        assert (self.subsession.max_amount == 100)
        assert (self.subsession.min_amount == 2)

        # start game
        self.submit(views.Introduction)
        self.submit(views.Question1, dict(
            training_answer_mine=1, training_answer_others=2))
        self.submit(views.Feedback1)

        # player 1: claim
        if self.player.id_in_group == 1:
            self.play_p1()

        # player 2: claim
        else:
            self.play_p2()

        self.submit(views.Results)
        self.submit(views.Question2, dict(feedback=3))

    def play_p1(self):
        self.submit(views.Claim, {"claim": random.randrange(2, 100)})

    def play_p2(self):
        self.submit(views.Claim, {"claim": random.randrange(2, 100)})
