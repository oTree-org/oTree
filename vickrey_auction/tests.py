# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        yield (views.Introduction)

        payoff = random.randint(
            Constants.min_allowable_bid, Constants.max_allowable_bid
        )
        yield (views.Bid, {"bid_amount": payoff})

        yield (views.Results)
