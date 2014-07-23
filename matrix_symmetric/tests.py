import ptree.test
import matrix_symmetric.views as views
from matrix_symmetric.utilities import ParticipantMixIn, MatchMixIn, SubsessionMixIn
import random


class ParticipantBot(ParticipantMixIn, ptree.test.ParticipantBot):

    def play(self):

        # random decision
        choice = random.choice((('A', 'A'), ('B', 'B')))[0]
        self.submit(views.Decision, {"decision": choice})

        #  results
        self.submit(views.Results)


class ExperimenterBot(SubsessionMixIn, ptree.test.ExperimenterBot):

    def play(self):
        pass