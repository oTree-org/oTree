# -*- coding: utf-8 -*-
import common_value_auction.models as models
from common_value_auction._builtin import Page, SubsessionWaitPage
from otree.common import Money


class Introduction(Page):

    template_name = 'common_value_auction/Introduction.html'

    def variables_for_template(self):
        return {'other_players_count': len(self.subsession.players)-1}


class Bid(Page):

    template_name = 'common_value_auction/Bid.html'

    form_model = models.Player
    form_fields = ['bid_amount']

    def variables_for_template(self):
        if self.player.item_value_estimate is None:
            self.player.item_value_estimate = self.treatment.generate_value_estimate()

        return {'item_value_estimate': self.player.item_value_estimate,
                'error_margin': self.treatment.estimate_error_margin,
                'min_bid': Money(self.treatment.min_allowable_bid),
                'max_bid': Money(self.treatment.max_allowable_bid)}


class ResultsWaitPage(SubsessionWaitPage):

    def after_all_players_arrive(self):
        self.subsession.set_winner()


class Results(Page):

    template_name = 'common_value_auction/Results.html'

    def variables_for_template(self):
        if self.player.payoff is None:
            self.player.set_payoff()

        return {'is_winner': self.player.is_winner,
                'is_greedy': self.treatment.item_value - self.player.bid_amount < 0,
                'bid_amount': self.player.bid_amount,
                'winning_bid': self.subsession.highest_bid(),
                'item_value': self.treatment.item_value,
                'payoff': self.player.payoff}


def pages():

    return [Introduction,
            Bid,
            ResultsWaitPage,
            Results]
