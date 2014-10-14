# -*- coding: utf-8 -*-
from __future__ import division
from . import views
from ._builtin import Bot
import random
from otree.common import Money, money_range
from .models import Constants
class PlayerBot(Bot):

    def play(self):

        # start
        self.submit(views.Introduction)

        # bid
        self.submit(views.Bid, {'bid_amount': random.choice(money_range(0, self.subsession.max_bid_amount))})

        # results
        self.submit(views.Results)