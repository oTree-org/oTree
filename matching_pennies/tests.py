# -*- coding: utf-8 -*-
from __future__ import division
from . import views
from ._builtin import Bot
import random
from otree.common import Currency, currency_range
from .models import Constants


class PlayerBot(Bot):

    def play(self):

        rounds = Constants.number_of_rounds
        round = self.subsession.round_number

        if round == 1:
            # only submitted on round 1
            self.submit(views.Introduction)
            self.submit(views.QuestionOne, {'training_question_1': 'Player 1 gets 0 points, Player 2 gets 0 points'})
            self.submit(views.FeedbackOne)

        # repeated for the no. of rounds
        self.submit(views.Choice, {"penny_side": random.choice(['Heads', 'Tails'])})
        self.submit(views.Results)

        # submitted in last round
        if round == rounds:
            self.submit(views.ResultsSummary)