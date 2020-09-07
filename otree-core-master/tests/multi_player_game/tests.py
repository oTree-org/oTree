# -*- coding: utf-8 -*-
from __future__ import division, absolute_import
from . import views
from otree.api import Bot


class PlayerBot(Bot):

    def play_round(self):

        if self.player.id_in_group == 1:
            yield (views.FieldOnOtherPlayer)
        yield (views.Results)

    def validate_play(self):
        pass
