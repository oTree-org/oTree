# -*- coding: utf-8 -*-
import ptree.test
from ptree.common import Money, money_range
import trust.views as views
from trust.utilities import Bot
import random


class ParticipantBot(Bot):

    def play(self):

        # basic assertions
        assert (self.treatment.amount_allocated == 1.00)
        assert (self.match.participants_per_match == 2)

        sent_amount = 0.5
        sent_back_amount = 0.7

        # start game
        self.submit(views.Introduction)

        # if p1, play send page
        if self.participant.index_among_participants_in_match == 1:
            self.play_p1()

        # else p2, play send back page
        else:
            self.play_p2()

        # finally, show results
        self.submit(views.Results)

    def play_p1(self):
        self.submit(views.Send,
                    {"sent_amount": 0.5})

    def play_p2(self):
        self.submit(views.SendBack, {'sent_back_amount': 0.7})



