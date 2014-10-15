# -*- coding: utf-8 -*-

import random

import otree.test
from otree.common import Money, money_range

from rock_paper_scissors import views, models
from rock_paper_scissors._builtin import Bot


class PlayerBot(Bot):

    def play(self):

        rounds = self.subsession.number_of_rounds
        round = self.subsession.round_number

        if round == 1:
            # only submitted on round 1
            answer = models.TRAINING_OPTIONS[0]["options"][
                models.TRAINING_OPTIONS[0]["answer"]
            ]
            self.submit(views.Introduction)
            self.submit(views.QuestionOne, {'training_question_1': answer})
            self.submit(views.FeedbackOne)

        # repeated for the no. of rounds
        self.submit(views.Choice, {"penny_side": random.choice(models.RPS)})
        self.submit(views.Results)

        # submitted in last round
        if round == rounds:
            self.submit(views.ResultsSummary)
