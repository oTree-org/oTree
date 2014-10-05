# -*- coding: utf-8 -*-
from __future__ import division
import private_value_auction.models as models
from private_value_auction._builtin import Page, WaitPage
from otree.common import Money


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
                'min_bid': Money(self.subsession.min_allowable_bid),
                'max_bid': Money(self.subsession.max_allowable_bid)}


class ResultsWaitPage(WaitPage):

    group = models.Match

    def after_all_players_arrive(self):
        self.match.set_winner()


class Results(Page):

    template_name = 'private_value_auction/Results.html'

    def variables_for_template(self):
        if self.player.payoff is None:
            self.player.set_payoff()

        return {'is_winner': self.player.is_winner,
                'is_greedy': self.player.private_value - self.player.bid_amount < 0,
                'bid_amount': self.player.bid_amount,
                'winning_bid': self.match.highest_bid(),
                'private_value': self.player.private_value,
                'payoff': self.player.payoff}


def pages():

    return [Introduction,
            Bid,
            ResultsWaitPage,
            Results]
