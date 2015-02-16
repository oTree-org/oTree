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
            self.submit(views.Introduction)
            value = 'Player 1 gets 0 points, Player 2 gets 0 points'
            self.submit(views.Question, {'training_question_1': value})
            self.submit(views.Feedback1)

        # repeated for the no. of rounds
        self.submit(views.Choice,
            {"penny_side": random.choice(['Heads', 'Tails'])}
        )
        self.submit(views.Results)

        # submitted in last round
        if round == rounds:
            self.submit(views.ResultsSummary)

    def validate_play(self):
        pass
