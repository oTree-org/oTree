import ptree.test
import matching_pennies.views as views
from matching_pennies.utilities import ParticipantMixin, ExperimenterMixin


class ParticipantBot(ParticipantMixin, ptree.test.ParticipantBot):

    def play(self):
        # intro to both players
        self.submit(views.Introduction)

        # both players chooses their penny side
        if self.participant.index_among_participants_in_match == 1:
            self.submit(views.Choice, {"penny_side": "head"})
        else:
            self.submit(views.Choice, {"penny_side": "tail"})

        # results after decisions
        self.submit(views.Results)


class ExperimenterBot(ExperimenterMixin, ptree.test.ExperimenterBot):

    def play(self):
        pass
