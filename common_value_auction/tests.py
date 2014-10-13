# -*- coding: utf-8 -*-
from __future__ import division
from . import views
from ._builtin import Bot
import random
from otree.common import Money, money_range

class PlayerBot(Bot):

    def play(self):

        # Introduction
        self.submit(views.Introduction)

        # player: bid
        self.submit(views.Bid, {"bid_amount": round(random.uniform(self.subsession.min_allowable_bid, self.subsession.max_allowable_bid), 1)})

        # results
        self.submit(views.Results)
