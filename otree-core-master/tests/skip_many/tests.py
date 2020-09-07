# -*- coding: utf-8 -*-
from __future__ import division

from otree.api import Bot

from . import views
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        if self.subsession.round_number == Constants.num_rounds:
            yield (views.MyPage)
            yield (views.Results)

    def validate_play(self):
        pass
