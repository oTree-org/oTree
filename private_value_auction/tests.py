import ptree.test
from ptree.common import Money, money_range
import private_value_auction.views as views
from private_value_auction.utilities import Bot
import random


class ParticipantBot(Bot):

    def play(self):

        # Introduction
        self.submit(views.Introduction)

        # bid
        self.submit(views.Bid, {"bid_amount": random.choice(self.match.bid_choices())})

        # results
        self.submit(views.Results)