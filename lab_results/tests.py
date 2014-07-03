import ptree.test
import lab_results.views as views
from lab_results.utilities import ParticipantMixin, ExperimenterMixin


class ParticipantBot(ParticipantMixin, ptree.test.ParticipantBot):

    def play(self):
        pass


class ExperimenterBot(ExperimenterMixin, ptree.test.ExperimenterBot):

    def play(self):
        pass
