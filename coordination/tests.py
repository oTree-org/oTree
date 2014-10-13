# -*- coding: utf-8 -*-
from __future__ import division
import coordination.views as views
from coordination._builtin import Bot
import random


class PlayerBot(Bot):

    def play(self):

        # random decision
        choice = random.choice(['A', 'B'])
        self.submit(views.Choice, {"choice": choice})

        # results
        self.submit(views.Results)
