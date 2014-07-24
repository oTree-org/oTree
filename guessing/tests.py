import ptree.test
import guessing.views as views
from guessing.utilities import ParticipantMixIn, MatchMixIn, SubsessionMixIn
import random


class ParticipantBot(ParticipantMixIn, ptree.test.ParticipantBot):

    def play(self):

        # start game
        self.submit(views.Introduction)

        # make your guess
        self.submit(views.Guess, {"guess_value": random.choice(range(0, 100))})

        self.submit(views.Results)

    def play_p2(self):
        self.submit(views.Guess, {"guess_value": random.choice(range(0, 100))})


class ExperimenterBot(SubsessionMixIn, ptree.test.ExperimenterBot):

    def play(self):
        self.submit(views.Experimenter)
