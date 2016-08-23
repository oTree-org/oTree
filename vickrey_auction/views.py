# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants


class Introduction(Page):
    pass


class Bid(Page):
    form_model = models.Player
    form_fields = ['bid_amount']


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_winner()
        self.group.set_payoffs()


class Results(Page):
    pass


page_sequence = [
    Introduction,
    Bid,
    ResultsWaitPage,
    Results]
