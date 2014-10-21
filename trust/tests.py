# -*- coding: utf-8 -*-
from __future__ import division
from . import views
from ._builtin import Bot
import random
from otree.common import Money, money_range
from .models import Constants

class PlayerBot(Bot):

    def play(self):

        assert (self.group.players_per_group == 2)

        # start game
        self.submit(views.Introduction)
        self.submit(views.Question1, dict(
            training_answer_x=1, training_answer_y=2))
        self.submit(views.Feedback1)

        # if p1, play send page
        if self.player.id_in_group == 1:
            self.play_p1()

        # else p2, play send back page
        else:
            self.play_p2()

        # finally, show results
        self.submit(views.Results)
        self.submit(views.Question2, dict(feedback=4))

    def play_p1(self):
        # random send amount

        self.submit(views.Send, {"sent_amount": 4})

    def play_p2(self):
        # random send back amount
        self.submit(views.SendBack, {'sent_back_amount': 8})
