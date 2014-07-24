import ptree.test
import coordination.views as views
from coordination.utilities import ParticipantMixIn


class ParticipantBot(ParticipantMixIn, ptree.test.ParticipantBot):

    def play(self):
        pass


