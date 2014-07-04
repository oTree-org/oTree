import ptree.test
import matrix.views as views
from matrix.utilities import ParticipantMixin, ExperimenterMixin

class ParticipantBot(ParticipantMixin, ptree.test.ParticipantBot):

    def play(self):
        pass

class ExperimenterBot(ExperimenterMixin, ptree.test.ExperimenterBot):

    def play(self):
        pass
