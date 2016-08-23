# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from ._builtin import Bot
from .models import Constants
from . import views


class PlayerBot(Bot):

    def play_round(self):
        yield (views.Introduction)

        # units to produce
        units = random.choice(range(0, Constants.max_units_per_player + 1))
        yield (views.Decide, {'units': units})

        # results
        yield (views.Results)

