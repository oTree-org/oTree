import otree.test
import common_value_auction.views as views
from common_value_auction.utilities import Bot
from otree.common import Money, money_range
import random


class PlayerBot(Bot):

    def play(self):

        # Introduction
        self.submit(views.Introduction)

        # player: bid
        self.submit(views.Bid, {"bid_amount": random.choice(self.match.bid_choices())})

        # results
        self.submit(views.Results)