import ptree.test
from ptree.common import Money, money_range
import survey.views as views
from survey.utilities import Bot


class ParticipantBot(Bot):

    def play(self):

        pass


class ExperimenterBot(SubsessionMixIn, ptree.test.ExperimenterBot):

    def play(self):

        pass
