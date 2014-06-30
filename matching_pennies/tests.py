import ptree.test
import matching_pennies.views as views
from matching_pennies.utilities import ParticipantMixin, ExperimenterMixin
import random


class ParticipantBot(ParticipantMixin, ptree.test.ParticipantBot):

    def play(self):

        # both players choose their heads or tails
        choice = random.choice(self.participant.PENNY_CHOICES)[0]
        if self.participant.index_among_participants_in_match == 1:
            self.submit(views.Choice, {"penny_side": choice})
        else:
            self.submit(views.Choice, {"penny_side": choice})

        # results after choices
        self.submit(views.Results)


class ExperimenterBot(ExperimenterMixin, ptree.test.ExperimenterBot):

    def play(self):

        pass
