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

            yield (views.Introduction)
            yield (views.Instructions)
            yield (
                views.Question1, {'understanding_question_1': 'P=2.5, N=2'}
            )
            yield (views.Feedback1)
            yield (views.Question2, {'understanding_question_2': '$8, $12'})
            yield (views.Feedback2)

        # randomize inputs: between the two players
        ran_num = random.randint(1,2)
        if ran_num == 1:
            yield (
                views.Order,
                {'order_type': 'Sell', 'sn': 1, 'sp': 2, 'bn': 0, 'bp': 0}
            )
        else:
            yield (
                views.Order,
                {'order_type': 'Buy', 'sn': 0, 'sp': 0, 'bn': 1, 'bp': 4}
            )

        yield (views.Transaction)
        yield (views.Dividend)

        # submitted in last round
        if roundn == Constants.num_rounds:
            yield (views.Results)

