import otree.test
from otree.common import Money, money_range
import guessing.views as views
from guessing._builtin import Bot
import random


class PlayerBot(Bot):

    def play(self):

        # start game
        self.submit(views.Introduction)

        # make your guess
        self.submit(views.Guess, {"guess_value": random.randint(0, 100)})

        self.submit(views.Results)

    def play_p2(self):
        self.submit(views.Guess, {"guess_value": random.randint(0, 100)})
