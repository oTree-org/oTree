import ptree.test
from ptree.common import Money, money_range
import stag_hunt.views as views
from stag_hunt.utilities import Bot

class ParticipantBot(Bot):

    def play(self):
        pass

class ExperimenterBot(ExperimenterMixIn, ptree.test.ExperimenterBot):

    def play(self):
        pass
