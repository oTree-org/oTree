# -*- coding: utf-8 -*-
from __future__ import division
from . import views
from ._builtin import Bot
import random
from otree.common import Money, money_range


class PlayerBot(Bot):

    def play(self):
        # compete price
        self.submit(views.Decide, {'price': random.choice(money_range(self.subsession.marginal_cost, self.subsession.maximum_price, 0.05))})

        # results
        self.submit(views.Results)
