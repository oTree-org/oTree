import ptree.test
import lab_results.views as views
from lab_results.utilities import ParticipantMixIn, MatchMixIn, SubsessionMixIn


class ParticipantBot(ParticipantMixIn, ptree.test.ParticipantBot):

    def play(self):
        pass


class ExperimenterBot(SubsessionMixIn, ptree.test.ExperimenterBot):

    def play(self):
        pass
