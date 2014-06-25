# -*- coding: utf-8 -*-
import ptree.test
import prisoner_minimal.views as views
from prisoner_minimal.utilities import ParticipantMixin, ExperimenterMixin


class ParticipantBot(ParticipantMixin, ptree.test.ParticipantBot):

    def play(self):

        # both players make decision
        if self.participant.index_among_participants_in_match == 1:
            self.submit(views.Decision, {"decision": "Compete"})
        else:
            self.submit(views.Decision, {"decision": "Cooperate"})

        # results after decisions
        self.submit(views.Results)


class ExperimenterBot(ExperimenterMixin, ptree.test.ExperimenterBot):

    def play(self):
        pass
