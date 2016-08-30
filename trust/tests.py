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
            yield (views.Send, {"sent_amount": 4})

        else:
            yield (views.SendBack, {'sent_back_amount': 8})

        yield (views.Results)
