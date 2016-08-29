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

        if self.player.id_in_group == 1:
            yield (views.Offer, {"kept": c(99)})
            assert self.player.payoff == c(99)
        else:
            assert self.player.payoff == c(1)
        yield (views.Results)
