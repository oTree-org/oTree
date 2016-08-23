# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):

        # start
        yield (views.Introduction)

        # request
        amount = random.randrange(Constants.amount_shared)
        yield (views.Request, {"request_amount": amount})

        # results
        yield (views.Results)

