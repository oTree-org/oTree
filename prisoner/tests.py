# -*- coding: utf-8 -*-
import ptree.test
import prisoner.views as views
from prisoner.utilities import ParticipantMixIn, ExperimenterMixIn
import random


class ParticipantBot(ParticipantMixIn, ptree.test.ParticipantBot):

    def play(self):

        # each player makes random decision
        self.submit(views.Decision, {"decision": random.choice(self.participant.DECISION_CHOICES)[0]})

        # submit results
        self.submit(views.Results)


class ExperimenterBot(ExperimenterMixIn, ptree.test.ExperimenterBot):

    def play(self):
        pass

