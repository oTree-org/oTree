# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from ._builtin import Bot
from .models import Constants
from . import views


class PlayerBot(Bot):

    def play_round(self):
        self.submit(views.Introduction)
        if self.player.id_in_group == 1:
            self.submit(views.Offer, {'amount_offered': c(10)})
        else:
            if self.group.strategy:
                self.submit(views.AcceptStrategy, {'response_{}'.format(int(offer)): True for offer in Constants.offer_choices})
            else:
                self.submit(views.Accept, {'offer_accepted': True})
        self.submit(views.Results)

    def validate_play(self):
        pass


