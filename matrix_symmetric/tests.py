import ptree.test
import matrix_symmetric.views as views
from matrix_symmetric.utilities import ParticipantMixin, ExperimenterMixin

class ParticipantBot(ParticipantMixin, ptree.test.ParticipantBot):

    def play(self):
        pass

class ExperimenterBot(ExperimenterMixin, ptree.test.ExperimenterBot):

    def play(self):
        pass
