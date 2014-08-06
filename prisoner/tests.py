# -*- coding: utf-8 -*-
import ptree.test
from ptree.common import Money, money_range
import prisoner.views as views
from prisoner.utilities import Bot
import random


class ParticipantBot(Bot):

    def play(self):

        # each player makes random decision
        self.submit(views.Decision, {"decision": random.choice(self.participant.DECISION_CHOICES)[0]})

        # submit results
        self.submit(views.Results)



