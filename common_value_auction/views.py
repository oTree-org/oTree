# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants

class Introduction(Page):

    template_name = 'common_value_auction/Introduction.html'

    def vars_for_template(self):
        return {'other_players_count': len(self.group.get_players())-1}


class Bid(Page):

    template_name = 'common_value_auction/Bid.html'

    form_model = models.Player
    form_fields = ['bid_amount']

    def vars_for_template(self):
        if self.player.item_value_estimate is None:
            self.player.item_value_estimate = self.group.generate_value_estimate()

        return {'item_value_estimate': self.player.item_value_estimate,
                'error_margin': Constants.estimate_error_margin,
                'min_bid': Constants.min_allowable_bid,
                'max_bid': Constants.max_allowable_bid}


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_winner()


class Results(Page):

    template_name = 'common_value_auction/Results.html'

    def vars_for_template(self):
        if self.player.payoff is None:
            self.player.set_payoff()

        return {'is_winner': self.player.is_winner,
                'is_greedy': self.group.item_value - self.player.bid_amount < 0,
                'bid_amount': self.player.bid_amount,
                'winning_bid': self.group.highest_bid(),
                'item_value': self.group.item_value,
                'payoff': self.player.payoff}


page_sequence = [Introduction,
            Bid,
            ResultsWaitPage,
            Results]
