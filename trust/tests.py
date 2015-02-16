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
        self.submit(views.Introduction)
        self.submit(
            views.Question1, {"training_answer_x": 1, "training_answer_y": 2}
        )
        self.submit(views.Feedback)

        # if p1, play send page
        if self.player.id_in_group == 1:
            self.submit(views.Send, {"sent_amount": 4})

        # else p2, play send back page
        else:
            self.submit(views.SendBack, {'sent_back_amount': 8})

        # finally, show results
        self.submit(views.Results)

    def validate_play(self):
        assert (Constants.players_per_group == 2)


