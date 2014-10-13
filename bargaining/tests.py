# -*- coding: utf-8 -*-
from __future__ import division
import bargaining.views as views
from bargaining._builtin import Bot
import random


class PlayerBot(Bot):

    def play(self):

        # start
        self.submit(views.Introduction)

        # request
        self.submit(views.Request, {"request_amount": random.choice(self.player.request_amount_choices())})

        # results
        self.submit(views.Results)
