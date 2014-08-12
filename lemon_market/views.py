# -*- coding: utf-8 -*-
import otree.views
import lemon_market.forms as forms
from lemon_market.utilities import Page, MatchWaitPage, SubsessionWaitPage



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

    def get_form_class(self):
        return forms.BidForm


class ResultsWaitPage(MatchWaitPage):

    def action(self):
        for p in self.match.players:
            p.set_payoff()


class Results(Page):

    template_name = 'lemon_market/Results.html'

    def variables_for_template(self):
        return {
            'payoff': self.player.payoff,
            'bid_amount': self.match.bid_amount,
            'random_value': self.match.random_value
        }


def pages():
    return [
        Introduction,
        Bid,
        ResultsWaitPage,
        Results
    ]