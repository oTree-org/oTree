import ptree.test
import trust.views as views
from trust.utilities import ParticipantMixin, ExperimenterMixin


class ParticipantBot(ParticipantMixin, ptree.test.ParticipantBot):

    def play(self):

        # basic assertions
        assert (self.treatment.amount_allocated == 100)
        assert (self.match.participants_per_match == 2)

        # start game
        self.submit(views.Introduction)

        # if p1, play send page
        if self.participant.index_among_participants_in_match == 1:
            self.play_p1()

        # else p2, send back page
        else:
            self.play_p2()

        # finally, show the results
        self.submit(views.Results)

    def play_p1(self):
        self.submit(views.Send, {"sent_amount": 100})

    def play_p2(self):
        self.submit(views.SendBack, {'sent_back_amount': 200})


class ExperimenterBot(ExperimenterMixin, ptree.test.ExperimenterBot):

    def play(self):
        pass
