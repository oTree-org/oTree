# -*- coding: utf-8 -*-
import volunteer_dilemma.views as views
from volunteer_dilemma._builtin import Bot
import random


class PlayerBot(Bot):

    def play(self):

        # decision
        self.submit(views.Decision, {"decision": random.choice(['Volunteer', 'Ignore'])})

        # results
        self.submit(views.Results)
