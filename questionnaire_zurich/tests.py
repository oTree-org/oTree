import ptree.test
import questionnaire_zurich.views as views
from questionnaire_zurich.utilities import ParticipantMixin, ExperimenterMixin

class ParticipantBot(ParticipantMixin, ptree.test.ParticipantBot):

    def play(self):
        pass

class ExperimenterBot(ExperimenterMixin, ptree.test.ExperimenterBot):

    def play(self):
        pass
