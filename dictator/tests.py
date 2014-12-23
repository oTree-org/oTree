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
        self.submit(views.Question1, {'training_participant1_payoff': 1,
                                      'training_participant2_payoff': 2})
        self.submit(views.Feedback1)

        # dictator
        if self.player.id_in_group == 1:
            self.submit(views.Offer, {"kept": random.randrange(100)})

        self.submit(views.Results)

    def validate_play(self):
        # basic assertions
        assert (Constants.allocated_amount == 100)
        assert (Constants.players_per_group == 2)

