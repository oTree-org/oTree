import ptree.test
from ptree.common import Money, money_range
import matrix_symmetric.views as views
from matrix_symmetric.utilities import Bot
import random


class ParticipantBot(Bot):

    def play(self):

        # random decision
        choice = random.choice((('A', 'A'), ('B', 'B')))[0]
        self.submit(views.Decision, {"decision": choice})

        #  results
        self.submit(views.Results)


