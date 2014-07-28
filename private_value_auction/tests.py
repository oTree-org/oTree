import ptree.test
import private_value_auction.views as views
from private_value_auction.utilities import Bot
import random


class ParticipantBot(Bot):

    def play(self):

        # Introduction
        self.submit(views.Introduction)

        # player 1: bid
        if self.participant.index_among_participants_in_match == 1:
            self.play_p1()

        # player 2: bid
        else:
            self.play_p2()

        self.submit(views.Results)

    def play_p1(self):
        self.submit(views.Bid, {"bid_amount": random.choice(self.match.bid_choices())})

    def play_p2(self):
        self.submit(views.Bid, {"bid_amount": random.choice(self.match.bid_choices())})


