import ptree.test
import volunteer_dilemma.views as views
from volunteer_dilemma.utilities import ParticipantMixIn, ExperimenterMixIn
import random


class ParticipantBot(ParticipantMixIn, ptree.test.ParticipantBot):

    def play(self):

        # decision
        self.submit(views.Decision, {"decision": random.choice(self.participant.DECISION_CHOICES)[0]})

        # results
        self.submit(views.Results)


class ExperimenterBot(ExperimenterMixIn, ptree.test.ExperimenterBot):

    def play(self):
        pass
