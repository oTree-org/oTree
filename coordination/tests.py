import otree.test
from otree.common import Money, money_range
import coordination.views as views
from coordination.utilities import Bot
import random


class PlayerBot(Bot):

    def play(self):

        # random decision
        choice = random.choice(['A', 'B'])
        self.submit(views.Choice, {"choice": choice})

        # results
        self.submit(views.Results)

