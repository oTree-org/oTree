# -*- coding: utf-8 -*-
from __future__ import division
from . import views
from ._builtin import Bot
import random
from otree.common import Money, money_range
from .models import Constants


class PlayerBot(Bot):

    def play(self):

        rounds = self.subsession.number_of_rounds
        round = self.subsession.round_number

        if round == 1:
            # only submitted in round 1

            self.submit(views.Introduction)
            self.submit(views.Instructions)
            self.submit(views.QuestionOne, {'understanding_question_1': 'P=2.5, N=2'})
            self.submit(views.FeedbackOne)
            self.submit(views.QuestionTwo, {'understanding_question_2': '$8, $12'})
            self.submit(views.FeedbackTwo)

        # randomize inputs: between the two players
        ran_num = random.randint(1,2)
        if ran_num == 1:
            self.submit(views.Order, {'order_type': 'Sell', 'sn': 3, 'sp': 2, 'bn': 0, 'bp': 0})
        else:
            self.submit(views.Order, {'order_type': 'Buy', 'sn': 0, 'sp': 0, 'bn': 3, 'bp': 4})

        self.submit(views.Transaction)

        self.submit(views.Dividend)

        # submitted in last round
        if round == rounds:
            self.submit(views.Results)

            # randomise feedback
            choices = ['Very well', 'Well', 'OK', 'Badly', 'Very badly']
            rand_choice = random.randint(0,4)

            self.submit(views.FeedbackQ, {'feedbackq': choices[rand_choice]})