# -*- coding: utf-8 -*-
import tragedy_of_the_commons_old.views as views
from tragedy_of_the_commons_old._builtin import Bot
from otree.common import Money, money_range
import random


class PlayerBot(Bot):

    def play(self):

        # introduction
        self.submit(views.Introduction)

        # decision
        self.submit(views.Decision, {"decision": random.choice(['cooperate', 'defect'])})

        # results
        self.submit(views.Results)
