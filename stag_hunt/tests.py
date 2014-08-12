import otree.test
from otree.common import Money, money_range
import stag_hunt.views as views
from stag_hunt.utilities import Bot
import random


class PlayerBot(Bot):

    def play(self):

        # random decision
        choice = random.choice((('Stag', 'Stag'), ('Hare', 'Hare')))[0]

        self.submit(views.Decide, {"decision": choice})

        # results
        self.submit(views.Results)
