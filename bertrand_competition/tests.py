# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        # compete price
        yield (views.Introduction)
        yield (views.Question1, {'training_my_profit': c(1)})
        yield (views.Feedback1)
        yield (views.Decide, {'price': c(30)})
        yield (views.Results)

