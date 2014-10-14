# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Money, money_range
from .models import Constants

class Introduction(Page):

    template_name = 'private_value_auction/Introduction.html'


class Bid(Page):

    template_name = 'private_value_auction/Bid.html'

    form_model = models.Player
    form_fields = ['bid_amount']

    def variables_for_template(self):
        if self.player.private_value is None:
            self.player.private_value = self.player.generate_private_value()

        return {'private_value': self.player.private_value,
                'min_bid': Money(Constants.min_allowable_bid),
                'max_bid': Money(Constants.max_allowable_bid)}


class ResultsWaitPage(WaitPage):

    scope = models.Group

    def after_all_players_arrive(self):
        self.group.set_winner()


class Results(Page):

    template_name = 'private_value_auction/Results.html'

    def variables_for_template(self):
        if self.player.payoff is None:
            self.player.set_payoff()

        return {'is_winner': self.player.is_winner,
                'is_greedy': self.player.private_value - self.player.bid_amount < 0,
                'bid_amount': self.player.bid_amount,
                'winning_bid': self.group.highest_bid(),
                'private_value': self.player.private_value,
                'payoff': self.player.payoff}


def pages():

    return [Introduction,
            Bid,
            ResultsWaitPage,
            Results]
