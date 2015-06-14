# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from ._builtin import Bot
from .models import Constants
from . import views


class PlayerBot(Bot):

    def play_round(self):
        # if p1, play send page
        if self.player.id_in_group == 1:
            self.submit(views.Send, {"sent_amount": 3})

        # else p2, play send back page
        else:
            self.submit(views.SendBack, {'sent_back_amount': 6})

        # finally, show results
        self.submit(views.Results)

    def validate_play(self):
        pass


