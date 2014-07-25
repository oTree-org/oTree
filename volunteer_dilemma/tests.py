import ptree.test
import volunteer_dilemma.views as views
from volunteer_dilemma.utilities import Bot
import random


class ParticipantBot(Bot):

    def play(self):

        # decision
        self.submit(views.Decision, {"decision": random.choice(self.participant.DECISION_CHOICES)[0]})

        # results
        self.submit(views.Results)
