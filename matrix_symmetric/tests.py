import ptree.test
import matrix_symmetric.views as views
from matrix_symmetric.utilities import ParticipantMixIn, ExperimenterMixIn


class ParticipantBot(ParticipantMixIn, ptree.test.ParticipantBot):

    def play(self):
        pass


class ExperimenterBot(ExperimenterMixIn, ptree.test.ExperimenterBot):

    def play(self):
        pass
