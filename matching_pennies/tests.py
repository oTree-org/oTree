# -*- coding: utf-8 -*-
from __future__ import division
from . import views
from ._builtin import Bot
import random
from otree.common import Currency as c, currency_range
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):

        rounds = Constants.num_rounds
        round = self.subsession.round_number

        if round == 1:
            # only submitted on round 1
            yield (views.Introduction)

        # repeated for the no. of rounds
        yield (views.Choice,
               {"penny_side": random.choice(['Heads', 'Tails'])}
               )
        yield (views.Results)

        # submitted in last round
        if round == rounds:
            yield (views.ResultsSummary)
