# -*- coding: utf-8 -*-
import otree.views
import otree.views.concrete
import common_value_auction.forms as forms
from common_value_auction.utilities import Page, MatchWaitPage, SubsessionWaitPage
from otree.common import Money, money_range


class Introduction(Page):

    template_name = 'common_value_auction/Introduction.html'


class Bid(Page):

    template_name = 'common_value_auction/Bid.html'

    def get_form_class(self):
        return forms.BidForm

    def variables_for_template(self):
        return {
            'prize_value': self.treatment.prize_value,
        }


class ResultsWaitPage(SubsessionWaitPage):

    def action(self):
        self.subsession.choose_winner()
        for p in self.subsession.players:
            p.set_payoff()


class Results(Page):

    template_name = 'common_value_auction/Results.html'

    def variables_for_template(self):
        return {
            'payoff': self.player.payoff,
            'bid_amount': self.player.bid_amount,
            'is_winner': self.player.is_winner
        }


def pages():
    return [
        Introduction,
        Bid,
        ResultsWaitPage,
        Results
    ]