# -*- coding: utf-8 -*-
from __future__ import division

import random
from otree.common import Currency as c, currency_range

from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        if self.subsession.round_number == 1:
            self.submit(views.Introduction)
            self.submit(
                views.Question1,
                {
                    'training_buyer_earnings': 1,
                    'training_seller1_earnings': 2,
                    'training_seller2_earnings': 3
                }
            )

            self.submit(views.Feedback1)
        if self.player.role() == 'buyer':
            self.submit(views.Purchase)
        else:
            self.submit(views.Production, {'price': 23, 'quality': 20})
        self.submit(views.Results)
        if self.subsession.round_number == Constants.num_rounds:
            self.submit(views.FinalResults)

    def validate_play(self):
        pass
