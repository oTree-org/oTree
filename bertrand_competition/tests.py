import ptree.test
import bertrand_competition.views as views
from bertrand_competition.utilities import ParticipantMixIn, MatchMixIn, SubsessionMixIn
import random


class ParticipantBot(ParticipantMixIn, ptree.test.ParticipantBot):

    def play(self):
        # start
        self.submit(views.Introduction)

        # compete price
        self.submit(views.Compete, {'price': random.choice(range(self.treatment.minimum_price+1, self.treatment.maximum_price, 1))})

        # results
        self.submit(views.Results)


class ExperimenterBot(SubsessionMixIn, ptree.test.ExperimenterBot):

    def play(self):
        pass
