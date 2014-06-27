# -*- coding: utf-8 -*-
import ptree.test
import prisoner_minimal.views as views
from prisoner_minimal.utilities import ParticipantMixin, ExperimenterMixin
import random


class ParticipantBot(ParticipantMixin, ptree.test.ParticipantBot):

    def play(self):

        # both players make decision
        if self.participant.index_among_participants_in_match == 1:
            self.submit(views.Decision, {"decision": random.choice(self.participant.DECISION_CHOICES[0])})
        else:
            self.submit(views.Decision, {"decision": random.choice(self.participant.DECISION_CHOICES[0])})

        # results after decisions
        self.submit(views.Results)


class ExperimenterBot(ExperimenterMixin, ptree.test.ExperimenterBot):

    def play(self):

        pass
