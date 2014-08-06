import ptree.test
from ptree.common import Money, money_range
import cournot_competition.views as views
from cournot_competition.utilities import Bot
import random


class ParticipantBot(Bot):

    def play(self):
        # start
        self.submit(views.Introduction)

        # compete quantity
        self.submit(views.Compete, {'quantity': random.choice(range(1, (self.treatment.total_capacity)/2))})

        # results
        self.submit(views.Results)


