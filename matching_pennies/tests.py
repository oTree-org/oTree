# -*- coding: utf-8 -*-
import otree.test
from otree.common import Money, money_range
import matching_pennies.views as views
from matching_pennies._builtin import Bot
import random


class PlayerBot(Bot):

    def play(self):

        rounds = self.subsession.number_of_rounds
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

        # FIXME: payoff is still None at the end of the subsession.