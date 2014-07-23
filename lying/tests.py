import ptree.test
import lying.views as views
from lying.utilities import ParticipantMixIn, MatchMixIn, SubsessionMixIn
import random


class ParticipantBot(ParticipantMixIn, ptree.test.ParticipantBot):

    def play(self):

        # assertions
        assert (self.treatment.number_of_flips == 10)
        assert (self.treatment.payoff_per_head == 10)

        # start game
        self.submit(views.Start)

        # coin flip
        self.submit(views.FlipCoins, {"number_of_heads": random.choice(range(1, 10, 1))})

        # results
        self.submit(views.Results)


class ExperimenterBot(SubsessionMixIn, ptree.test.ExperimenterBot):

    def play(self):
        pass