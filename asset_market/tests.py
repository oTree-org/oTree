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
        self.submit(views.Introduction)

        self.submit(views.Instructions)

        self.submit(views.QuestionOne, {'understanding_question_1': 'P=2.5, N=2'})

        self.submit(views.FeedbackOne)

        self.submit(views.QuestionTwo, {'understanding_question_2': '$8, $12'})

        self.submit(views.FeedbackTwo)

        self.submit(views.BuyOrder, {'bn': 4, 'bp': 0.50})

        self.submit(views.SellOrder, {'sn': 3, 'sp': 0.40})

        self.submit(views.Transaction)

        self.submit(views.Dividend)

        self.submit(views.Results)