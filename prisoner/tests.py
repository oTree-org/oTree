# -*- coding: utf-8 -*-
from __future__ import division
import prisoner.views as views
from prisoner._builtin import Bot
import random


class PlayerBot(Bot):

    def play(self):

        self.submit(views.Introduction)

        self.submit(views.QuestionOne, {'training_question_1': 'Alice gets 300 points, Bob gets 0 points'})

        self.submit(views.FeedbackOne)

        self.submit(views.Decision, {"decision": random.choice(['Cooperate', 'Defect'])})

        self.submit(views.Results)
        
        # FIXME: payoff is still None at the end of the subsession
