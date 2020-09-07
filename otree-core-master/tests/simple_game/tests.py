# -*- coding: utf-8 -*-
from __future__ import division
from . import views
from otree.api import Bot


class PlayerBot(Bot):

    def play_round(self):
        yield (views.MyPage, {'my_field': 1})
        yield (views.Results)

    def validate_play(self):
        pass
