import ptree.test
import bargaining.views as views
from bargaining.utilities import ParticipantMixIn, ExperimenterMixIn


class ParticipantBot(ParticipantMixIn, ptree.test.ParticipantBot):

    def play(self):
        pass


class ExperimenterBot(ExperimenterMixIn, ptree.test.ExperimenterBot):

    def play(self):
        pass
