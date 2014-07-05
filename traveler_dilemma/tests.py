import ptree.test
import traveler_dilemma.views as views
from traveler_dilemma.utilities import ParticipantMixIn, ExperimenterMixIn
import random


class ParticipantBot(ParticipantMixIn, ptree.test.ParticipantBot):

    def play(self):

        # basic assertions
        assert (self.treatment.max_amount == 100)
        assert (self.treatment.min_amount == 20)

        # start game
        self.submit(views.Introduction)

        # player 1: claim
        if self.participant.index_among_participants_in_match == 1:
            self.play_p1()

        # player 2: claim
        else:
            self.play_p2()

        self.submit(views.Results)
        print self.participant.payoff

    def play_p1(self):
        self.submit(views.Claim, {"claim": random.choice(self.match.claim_choices())})

    def play_p2(self):
        self.submit(views.Claim, {"claim": random.choice(self.match.claim_choices())})


class ExperimenterBot(ExperimenterMixIn, ptree.test.ExperimenterBot):

    def play(self):
        pass

