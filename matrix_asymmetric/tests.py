import ptree.test
import matrix_asymmetric.views as views
from matrix_asymmetric.utilities import Bot
import random


class ParticipantBot(Bot):

    def play(self):

        # random decision
        choice = random.choice((('A', 'A'), ('B', 'B')))[0]
        self.submit(views.Decision, {"decision": choice})

        #  results
        self.submit(views.Results)


