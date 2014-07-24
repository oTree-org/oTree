import ptree.test
import battle_of_the_sexes.views as views
from battle_of_the_sexes.utilities import ParticipantMixIn, ExperimenterMixIn

class ParticipantBot(ParticipantMixIn, ptree.test.ParticipantBot):

    def play(self):
        pass

class ExperimenterBot(ExperimenterMixIn, ptree.test.ExperimenterBot):

    def play(self):
        pass
