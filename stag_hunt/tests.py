# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        yield (views.Introduction)
        yield (views.Question, {
            "training_question_1_my_payoff": random.randint(0, 100),
            "training_question_1_other_payoff": random.randint(0, 100),
        })
        yield (views.Feedback)
        yield (
            views.Decide, {"decision": random.choice(['Stag', 'Hare'])}
        )
        yield (views.Results)

