# -*- coding: utf-8 -*-
import trust.views as views
from trust.utilities import Bot
import random


class PlayerBot(Bot):

    def play(self):

        # basic assertions
        assert (self.treatment.amount_allocated == 1.00)
        assert (self.match.players_per_match == 2)

        # start game
        self.submit(views.Introduction)

        # if p1, play send page
        if self.player.index_among_players_in_match == 1:
            self.play_p1()

        # else p2, play send back page
        else:
            self.play_p2()

        # finally, show results
        self.submit(views.Results)

    def play_p1(self):
        # random send amount

        self.submit(views.Send,
                    {"sent_amount": 0.1})

    def play_p2(self):
        # random send back amount
        self.submit(views.SendBack, {'sent_back_amount': 0.2})
