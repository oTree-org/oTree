import ptree.test
from ptree.common import Money, money_range
import coordination.views as views
from coordination.utilities import Bot
import random


class ParticipantBot(Bot):

    def play(self):

        # random decision
        choice = random.choice((('A', 'A'), ('B', 'B')))[0]
        self.submit(views.Choice, {"choice": choice})

        # results
        self.submit(views.Results)

