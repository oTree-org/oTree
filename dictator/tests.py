import ptree.test
import dictator.views as views
from dictator.utilities import ParticipantMixin, ExperimenterMixin


class ParticipantBot(ParticipantMixin, ptree.test.ParticipantBot):

    def play(self):

        # basic assertions
        assert (self.treatment.allocated_amount == 100)
        assert (self.match.participants_per_match == 2)

        # start game
        self.submit(views.Introduction)

        # if p1, play offer
        if self.participant.index_among_participants_in_match == 1:
            self.play_p1()

        # Show the results
        self.submit(views.Results)
        print self.participant.payoff

    def play_p1(self):
        self.submit(views.Offer, {"offer_amount": 25})
        print self.treatment.allocated_amount


class ExperimenterBot(ExperimenterMixin, ptree.test.ExperimenterBot):

    def play(self):
        pass

