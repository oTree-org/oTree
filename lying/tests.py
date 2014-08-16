import otree.test
from otree.common import Money, money_range
import lying.views as views
from lying.utilities import Bot
import random


class PlayerBot(Bot):

    def play(self):

        # assertions
        #assert (self.treatment.number_of_flips == 10)
        assert (self.treatment.payoff_per_head == 0.10)

        # coin flip
        self.submit(views.FlipCoins, {"number_of_heads": random.randint(0, 10)})

        # results
        self.submit(views.Results)


