import otree.test
from otree.common import Money, money_range
import survey.views as views
from survey.utilities import Bot


class ParticipantBot(Bot):

    def play(self):

        pass


class ExperimenterBot(SubsessionMixIn, otree.test.ExperimenterBot):

    def play(self):

        pass
