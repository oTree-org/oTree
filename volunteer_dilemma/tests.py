# -*- coding: utf-8 -*-
import volunteer_dilemma.views as views
from volunteer_dilemma._builtin import Bot
import random


class PlayerBot(Bot):

    def play(self):

        # decision
        self.submit(views.Decision, {"volunteer": bool(random.getrandbits(1))})

        # results
        self.submit(views.Results)
