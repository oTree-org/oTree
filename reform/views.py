# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Contribute(Page):

    def vars_for_template(self):

        return {
            'get_round_number': self.group.num_reforms,
            'unfortunate': self.group.reformed_player
        }

class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.reform()
        self.group.payoffs()


class Results(Page):

    def vars_for_template(self):

        return {
            'player_payoff': sum([p.payoff for p in self.player.in_all_rounds()])
        }

page_sequence =[
    Contribute,
    ResultsWaitPage,
    Results
]
