import otree.test
from otree.common import Money, money_range
import matrix_asymmetric.views as views
from matrix_asymmetric._builtin import Bot
import random


class PlayerBot(Bot):

    def play(self):

        # random decision
        choice = random.choice(['A','B'])
        self.submit(views.Decision, {"decision": choice})

        #  results
        self.submit(views.Results)


