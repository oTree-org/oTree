# -*- coding: utf-8 -*-
from __future__ import division

import random
from otree.common import Currency as c, currency_range

from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        if self.subsession.round_number == 1:
            yield (views.Introduction)
        if self.player.role() == 'buyer':
            yield (views.Purchase)
        else:
            yield (views.Production, {'price': 23, 'quality': 20})
        yield (views.Results)
        if self.subsession.round_number == Constants.num_rounds:
            yield (views.FinalResults)

