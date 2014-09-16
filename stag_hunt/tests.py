# -*- coding: utf-8 -*-
import stag_hunt.views as views
from stag_hunt._builtin import Bot
import random


class PlayerBot(Bot):

    def play(self):

        # random decision
        choice = random.choice(['Stag', 'Hare'])

        self.submit(views.Decide, {"decision": choice})

        # results
        self.submit(views.Results)
