# -*- coding: utf-8 -*-
from __future__ import division
from . import views
from ._builtin import Bot
import random
from otree.common import Money, money_range
from .models import Constants


class PlayerBot(Bot):

    def play(self):
        # TODO : work in progress

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
            self.submit(views.Order, {'sn': 4, 'sp': 5, 'bn': 0, 'bp': 0})
        else:
            self.submit(views.Order, {'sn': 0, 'sp': 0, 'bn': 4, 'bp': 6})

        self.submit(views.Transaction)

        self.submit(views.Dividend)
        # FIXME: tests failing at this point:
        # reason: Exception: Response status code: 302 (expected 200)
        # probable solution: include 302 response in otree-core tests, to cater for games with multiple rounds
        # and exempted pages in some rounds

        # submitted in last round
        if round == rounds:
            self.submit(views.Results)
            self.submit(views.FeedbackQ, {'feedbackq': 'Well'})