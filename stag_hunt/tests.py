import ptree.test
import stag_hunt.views as views
from stag_hunt.utilities import ParticipantMixIn, ExperimenterMixIn

class ParticipantBot(ParticipantMixIn, ptree.test.ParticipantBot):

    def play(self):
        pass

class ExperimenterBot(ExperimenterMixIn, ptree.test.ExperimenterBot):

    def play(self):
        pass
