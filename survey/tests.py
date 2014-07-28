import ptree.test
import survey.views as views
from survey.utilities import Bot


class ParticipantBot(Bot):

    def play(self):

        pass


class ExperimenterBot(SubsessionMixIn, ptree.test.ExperimenterBot):

    def play(self):

        pass
