# -*- coding: utf-8 -*-
from __future__ import division
import bertrand_competition.views as views
from bertrand_competition._builtin import Bot
import random
from otree.common import money_range


class PlayerBot(Bot):

    def play(self):
        # compete price
        self.submit(views.Decide, {'price': random.choice(money_range(self.subsession.marginal_cost + 0.01, self.subsession.maximum_price))})

        # results
        self.submit(views.Results)
