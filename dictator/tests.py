import ptree.test
import dictator.views as views
from dictator.utilities import ParticipantMixIn, ExperimenterMixIn
import random


class ParticipantBot(ParticipantMixIn, ptree.test.ParticipantBot):

    def play(self):

        # basic assertions
        assert (self.treatment.allocated_amount == 100)
        assert (self.match.participants_per_match == 2)

        # start game
        self.submit(views.Introduction)

        # dictator
        if self.participant.index_among_participants_in_match == 1:
            self.play_p1()

        self.submit(views.Results)

    def play_p1(self):

        self.submit(views.Offer, {"offer_amount": random.choice(self.match.offer_choices())})


class ExperimenterBot(ExperimenterMixIn, ptree.test.ExperimenterBot):

    def play(self):
        pass
