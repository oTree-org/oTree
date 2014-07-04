import ptree.test
import matrix_asymmetric.views as views
from matrix_asymmetric.utilities import ParticipantMixin, ExperimenterMixin

class ParticipantBot(ParticipantMixin, ptree.test.ParticipantBot):

    def play(self):
        pass

class ExperimenterBot(ExperimenterMixin, ptree.test.ExperimenterBot):

    def play(self):
        pass
