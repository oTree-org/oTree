# -*- coding: utf-8 -*-
import ptree.test
import prisoner.views as views
from prisoner.utilities import ParticipantMixin, ExperimenterMixin
import random


class ParticipantBot(ParticipantMixin, ptree.test.ParticipantBot):

    def play(self):

        # each player makes random decision
        self.submit(views.Decision, {"decision": random.choice(self.participant.DECISION_CHOICES)[0]})

        # submit results
        self.submit(views.Results)


class ExperimenterBot(ExperimenterMixin, ptree.test.ExperimenterBot):

    def play(self):

        self.submit(views.ExperimenterIntroduction)
