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
        assert (Constants.allocated_amount == 100)
        assert (self.group.players_per_group == 2)

        # start game
        self.submit(views.Introduction)
        self.submit(views.Question1, {'training_participant1_payoff': 1,
                                      'training_participant2_payoff': 2})
        self.submit(views.Feedback1)

        # dictator
        if self.player.id_in_group == 1:
            self.play_p1()

        self.submit(views.Results)
        self.submit(views.FeedbackQ, {'feedback': 3})

    def play_p1(self):

        self.submit(views.Offer, {"kept": random.randrange(100)})
