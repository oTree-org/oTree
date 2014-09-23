# -*- coding: utf-8 -*-
import otree.views
import lemon_marketold.forms as forms
from lemon_marketold._builtin import Page, MatchWaitPage, SubsessionWaitPage



class Introduction(Page):

    template_name = 'lemon_marketold/Introduction.html'

    def variables_for_template(self):
        return {
            'payoff': self.player.payoff,
        }


class Bid(Page):

    def participate_condition(self):
        return True

    template_name = 'lemon_marketold/Bid.html'

    def get_form_class(self):
        return forms.BidForm


class ResultsWaitPage(MatchWaitPage):

    def after_all_players_arrive(self):
        for p in self.match.players:
            p.set_payoff()


class Results(Page):

    template_name = 'lemon_marketold/Results.html'

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