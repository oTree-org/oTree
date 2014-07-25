# -*- coding: utf-8 -*-
import private_value_auction.forms as forms
from private_value_auction.utilities import Page, MatchWaitPage, SubsessionWaitPage
from ptree.common import currency


class Introduction(Page):

    template_name = 'private_value_auction/Introduction.html'


class Bid(Page):

    template_name = 'private_value_auction/Bid.html'

    def get_form_class(self):
        return forms.BidForm

    def variables_for_template(self):
        return {
            'price_value': currency(self.treatment.price_value),
        }

class ResultsWaitPage(SubsessionWaitPage):

    def action(self):
        self.subsession.choose_winner()
        for p in self.subsession.participants():
            p.set_payoff()


class Results(Page):

    template_name = 'private_value_auction/Results.html'

    def variables_for_template(self):
        return {
            'payoff': currency(self.participant.payoff),
            'bid_amount': currency(self.participant.bid_amount),
            'is_winner': self.participant.is_winner
        }


def pages():
    return [
        Introduction,
        Bid,
        ResultsWaitPage,
        Results
    ]