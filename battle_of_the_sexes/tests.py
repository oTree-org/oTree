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
        yield (views.Question1, {
            "training_question_1_husband": random.randint(0, 100),
            "training_question_1_wife": random.randint(0, 100),
        })
        yield (views.Feedback1)

        yield (
            views.Decide, {"decision": random.choice(['Football', 'Opera'])}
        )

        # results
        yield (views.Results)

