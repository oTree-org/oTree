import ptree.test
import survey.views as views
from survey.utilities import ParticipantMixin, ExperimenterMixin


class ParticipantBot(ParticipantMixin, ptree.test.ParticipantBot):

    def play(self):

        pass


class ExperimenterBot(ExperimenterMixin, ptree.test.ExperimenterBot):

    def play(self):

        pass
