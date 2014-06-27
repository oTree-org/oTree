import ptree.test
import public_goods.views as views
from public_goods.utilities import ParticipantMixin, ExperimenterMixin


class ParticipantBot(ParticipantMixin, ptree.test.ParticipantBot):

    def play(self):

        # all players
        self.submit(views.Introduction)

        # each contribute some amount
        if self.participant.index_among_participants_in_match == 1:
            self.submit(views.Contribute, {"contributed_amount": 50})
        elif self.participant.index_among_participants_in_match == 2:
            self.submit(views.Contribute, {"contributed_amount": 150})
        elif self.participant.index_among_participants_in_match == 3:
            self.submit(views.Contribute, {"contributed_amount": 200})
        elif self.participant.index_among_participants_in_match == 4:
            self.submit(views.Contribute, {"contributed_amount": 250})

        # show results for all
        self.submit(views.Results)


class ExperimenterBot(ExperimenterMixin, ptree.test.ExperimenterBot):

    def play(self):

        self.submit(views.ExperimenterPage)
