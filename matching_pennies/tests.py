import otree.test
from otree.common import Money, money_range
import matching_pennies.views as views
from matching_pennies._builtin import Bot
import random


class PlayerBot(Bot):

    def play(self):

        # both players choose their heads or tails
        choice = random.choice(['Heads', 'Tails'])
        self.submit(views.Choice, {"penny_side": choice})

        # results after choices
        self.submit(views.Results)
