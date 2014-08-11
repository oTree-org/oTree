import ptree.test
import tragedy_of_the_commons.views as views
from tragedy_of_the_commons.utilities import Bot
from ptree.common import Money, money_range
import random


class ParticipantBot(Bot):

    def play(self):

        # introduction
        self.submit(views.Introduction)

        # decision
        self.submit(views.Decision, {"decision": random.choice((('cooperate', 'cooperate'), ('defect', 'defect')))[0]})

        # results
        self.submit(views.Results)