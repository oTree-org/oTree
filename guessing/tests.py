import ptree.test
import guessing.views as views
from guessing.utilities import Bot
import random


class ParticipantBot(Bot):

    def play(self):

        # start game
        self.submit(views.Introduction)

        # make your guess
        self.submit(views.Guess, {"guess_value": random.choice(range(0, 100))})

        self.submit(views.Results)

    def play_p2(self):
        self.submit(views.Guess, {"guess_value": random.choice(range(0, 100))})
