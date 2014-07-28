import ptree.test
import lemon_market.views as views
from lemon_market.utilities import Bot
import random


class ParticipantBot(Bot):

    def play(self):

        # start
        self.submit(views.Introduction)

        # bid
        self.submit(views.Bid, {'bid_amount': random.choice(range(0, self.treatment.max_bid_amount))})

        # results
        self.submit(views.Results)