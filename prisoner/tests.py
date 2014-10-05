# -*- coding: utf-8 -*-
from __future__ import division
import prisoner.views as views
from prisoner._builtin import Bot
import random


class PlayerBot(Bot):

    def play(self):

        # each player makes random decision
        decision = random.choice(['Cooperate', 'Defect'])

        self.submit(views.Decision, {"decision": decision})

        # submit results
        self.submit(views.Results)
