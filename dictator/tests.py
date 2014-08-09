import ptree.test
from ptree.common import Money, money_range
import dictator.views as views
from dictator.utilities import Bot
import random


class ParticipantBot(Bot):

    def play(self):

        # basic assertions
        assert (self.treatment.allocated_amount == 1.0)
        assert (self.match.participants_per_match == 2)

        # start game
        self.submit(views.Introduction)

        # dictator
        if self.participant.index_among_participants_in_match == 1:
            self.play_p1()

        self.submit(views.Results)

    def play_p1(self):
        self.submit(views.Offer, {"offer_amount": random.choice(self.match.offer_choices())})


