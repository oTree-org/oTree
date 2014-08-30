# -*- coding: utf-8 -*-
import matrix_symmetric.views as views
from matrix_symmetric._builtin import Bot
import random


class PlayerBot(Bot):

    def play(self):

        # random decision
        choice = random.choice(['A', 'B'])
        self.submit(views.Decision, {"decision": choice})

        #  results
        self.submit(views.Results)
