import ptree.test
import survey.views as views
from survey.utilities import ParticipantMixIn, MatchMixIn, SubsessionMixIn


class ParticipantBot(ParticipantMixIn, ptree.test.ParticipantBot):

    def play(self):

        pass


class ExperimenterBot(SubsessionMixIn, ptree.test.ExperimenterBot):

    def play(self):

        pass
