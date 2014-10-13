# -*- coding: utf-8 -*-
from __future__ import division
from . import views
from ._builtin import Bot
import random
from otree.common import Money, money_range


class PlayerBot(Bot):

    def play(self):

        # basic assertions
        assert (self.subsession.allocated_amount == 1.0)
        assert (self.group.players_per_group == 2)

        # start game
        self.submit(views.Introduction)

        # dictator
        if self.player.id_in_group == 1:
            self.play_p1()

        self.submit(views.Results)

    def play_p1(self):

        self.submit(views.Offer, {"offer_amount": random.choice(self.group.offer_amount_choices())})
