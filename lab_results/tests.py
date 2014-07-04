import ptree.test
import lab_results.views as views
from lab_results.utilities import ParticipantMixIn, ExperimenterMixIn


class ParticipantBot(ParticipantMixIn, ptree.test.ParticipantBot):

    def play(self):
        pass


class ExperimenterBot(ExperimenterMixIn, ptree.test.ExperimenterBot):

    def play(self):
        pass
