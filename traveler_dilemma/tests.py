# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):

        # start game
        yield (views.Introduction)

        claim = random.randrange(Constants.min_amount, Constants.max_amount)
        yield (views.Claim, {"claim": claim})

        yield (views.Results)

