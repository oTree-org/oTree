# -*- coding: utf-8 -*-
import cournot_competition.views as views
from cournot_competition._builtin import Bot
import random


class PlayerBot(Bot):

    def play(self):

        # units to produce
        self.submit(views.Decide, {'units': random.choice(range(0, self.treatment.max_units_per_player() + 1))})

        # results
        self.submit(views.Results)
