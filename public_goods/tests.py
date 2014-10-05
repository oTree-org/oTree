# -*- coding: utf-8 -*-
from __future__ import division
import public_goods.views as views
from public_goods._builtin import Bot
import random


class PlayerBot(Bot):

    def play(self):

        # all players
        self.submit(views.Introduction)

        # each player contributes random amount
        self.submit(views.Contribute, {"contribution": random.choice(self.subsession.contribute_choices())})

        # submit results page
        self.submit(views.Results)
