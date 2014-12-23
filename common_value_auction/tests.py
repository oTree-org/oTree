# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):

        # Introduction
        self.submit(views.Introduction)

        # player: bid
        bid_amount = random.choice(
            currency_range(
                Constants.min_allowable_bid, Constants.max_allowable_bid, 1
            )
        )
        self.submit(views.Bid, {"bid_amount": bid_amount})

        # results
        self.submit(views.Results)

    def validate_play(self):
        pass
