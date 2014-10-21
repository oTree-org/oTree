# -*- coding: utf-8 -*-
from __future__ import division
from . import views
from ._builtin import Bot
import random
from otree.common import Money, money_range


class PlayerBot(Bot):

    def play(self):
        if self.subsession.round_number == 1:
            self.submit(views.Introduction)
            self.submit(views.Question1, dict(
                training_buyer_earnings=1, training_seller1_earnings=2,
                training_seller2_earnings=3))
            self.submit(views.Feedback1)
        if self.player.role() == 'buyer':
            self.submit(views.Purchase)
        else:
            self.submit(views.Production, dict(price=23, quality=20))
        self.submit(views.Results)
        if self.subsession.round_number == self.subsession.number_of_rounds:
            self.submit(views.FinalResults)
            self.submit(views.FeedbackQ, dict(feedback=5))
