# -*- coding: utf-8 -*-
import ptree.test
import trust.views as views
from trust.utilities import ParticipantMixin, ExperimenterMixin
import random


class ParticipantBot(ParticipantMixin, ptree.test.ParticipantBot):

    def play(self):

        # basic assertions
        assert (self.treatment.amount_allocated == 100)
        assert (self.match.participants_per_match == 2)

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

        #
        #  work in progress
        #   print payoffs of all participant pairs, for each match
        #
        #
        #for match in self.subsession.matches():
        #    for player in match.participants():
        #        print "Payoff P{} = {}".format(player.index_among_participants_in_match, player.payoff)

    def play_p1(self):
        self.submit(views.Send, {"sent_amount": random.choice(self.match.send_choices())})

    def play_p2(self):
        self.submit(views.SendBack, {'sent_back_amount': random.choice(self.match.send_back_choices())})


class ExperimenterBot(ExperimenterMixin, ptree.test.ExperimenterBot):

    def play(self):

        pass
