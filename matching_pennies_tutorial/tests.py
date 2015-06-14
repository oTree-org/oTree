# -*- coding: utf-8 -*-
from __future__ import division
from . import views
from ._builtin import Bot
import random
from otree.common import Currency as c, currency_range
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):

        self.submit(
            views.Choice,
            {"penny_side": random.choice(['Heads', 'Tails'])}
        )

        # submitted in last round
        if self.subsession.round_number == Constants.num_rounds:
            self.submit(views.ResultsSummary)

    def validate_play(self):
        pass