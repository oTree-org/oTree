# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Money, money_range

class Introduction(Page):

    template_name = 'lemon_market/Introduction.html'

    def variables_for_template(self):
        return {
            'payoff': self.player.payoff,
        }


class Bid(Page):

    def participate_condition(self):
        return True

    template_name = 'lemon_market/Bid.html'

    form_model = models.Group
    form_fields = ['bid_amount']


class ResultsWaitPage(WaitPage):

    scope = models.Group

    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_payoff()


class Results(Page):

    template_name = 'lemon_market/Results.html'

    def variables_for_template(self):
        return {
            'payoff': self.player.payoff,
            'bid_amount': self.group.bid_amount,
            'random_value': self.group.random_value
        }


def pages():
    return [
        Introduction,
        Bid,
        ResultsWaitPage,
        Results
    ]