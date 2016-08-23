# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from ._builtin import Bot
from .models import Constants
from . import views


class PlayerBot(Bot):
    def play_round(self):
        # start game
        yield (views.Introduction)

        # dictator
        if self.player.id_in_group == 1:
            yield (views.Offer, {"kept": random.randrange(100)})

        yield (views.Results)
