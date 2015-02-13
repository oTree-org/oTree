# -*- coding: utf-8 -*-
from __future__ import division

import random
import time

from otree.common import Currency as c, currency_range

from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):

        roundn = self.subsession.round_number

        if roundn == 1:
            #only submitted in round 1

            self.submit(views.Introduction)
            self.submit(views.Instructions)
            self.submit(
                views.Question1, {'understanding_question_1': 'P=2.5, N=2'}
            )
            self.submit(views.Feedback1)
            self.submit(views.Question2, {'understanding_question_2': '$8, $12'})
            self.submit(views.Feedback2)

        # randomize inputs: between the two players
        ran_num = random.randint(1,2)
        if ran_num == 1:
            self.submit(
                views.Order,
                {'order_type': 'Sell', 'sn': 1, 'sp': 2, 'bn': 0, 'bp': 0}
            )
        else:
            self.submit(
                views.Order,
                {'order_type': 'Buy', 'sn': 0, 'sp': 0, 'bn': 1, 'bp': 4}
            )

        self.submit(views.Transaction)
        self.submit(views.Dividend)

        # submitted in last round
        if roundn == Constants.num_rounds:
            self.submit(views.Results)

    def validate_play(self):
        pass
