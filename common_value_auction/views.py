# -*- coding: utf-8 -*-
import common_value_auction.forms as forms
from common_value_auction._builtin import Page, SubsessionWaitPage
from otree.common import Money


class Introduction(Page):

    template_name = 'common_value_auction/Introduction.html'

    def variables_for_template(self):
        return {'other_players_count': len(self.subsession.players)-1}


class Bid(Page):

    template_name = 'common_value_auction/Bid.html'

    def get_form_class(self):
        return forms.BidForm

    def variables_for_template(self):
        if self.player.item_value_estimate is None:
            self.player.item_value_estimate = self.treatment.generate_value_estimate()

        return {'item_value_estimate': self.player.item_value_estimate,
                'error_margin': self.treatment.item_value_error_margin,
                'min_bid': Money(self.treatment.item_value_min),
                'max_bid': Money(self.treatment.item_value_max)}


class Results(Page):

    template_name = 'common_value_auction/Results.html'

    def variables_for_template(self):
        if all(p.payoff is None for p in self.subsession.players):
            self.treatment.set_payoffs()

        return {'payoff': self.player.payoff,
                'bid_amount': self.player.bid_amount,
                'is_winner': self.player.is_winner}


def pages():

    return [Introduction,
            Bid,
            SubsessionWaitPage,
            Results]
