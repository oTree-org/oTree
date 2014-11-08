# -*- coding: utf-8 -*-
from __future__ import division
from . import views
from ._builtin import Bot
import random
from otree.common import Currency as c, currency_range
from .models import Constants


class PlayerBot(Bot):

    def play(self):

        # Introduction
        self.submit(views.Introduction)

        # player: bid
        self.submit(views.Bid, {"bid_amount": random.choice(currency_range(Constants.min_allowable_bid, Constants.max_allowable_bid, 1))})

        # results
        self.submit(views.Results)
