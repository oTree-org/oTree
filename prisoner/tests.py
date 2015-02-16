# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from ._builtin import Bot
from .models import Constants
from . import views


class PlayerBot(Bot):

    def play_round(self):

        self.submit(views.Introduction)

        self.submit(
            views.Question,
            {'training_question_1': 'Alice gets 300 points, Bob gets 0 points'}
        )

        self.submit(views.Feedback1)

        self.submit(
            views.Decision,
            {"decision": random.choice(['Cooperate', 'Defect'])}
        )

        self.submit(views.Results)

    def validate_play(self):
        pass
