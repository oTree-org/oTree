# -*- coding: utf-8 -*-
import prisoner.views as views
from prisoner.utilities import Bot
import random


class PlayerBot(Bot):

    def play(self):

        # each player makes random decision
        decision = random.choice((('Cooperate', 'Cooperate'), ('Defect', 'Defect')))[0]

        self.submit(views.Decision, {"decision": decision})

        # submit results
        self.submit(views.Results)
