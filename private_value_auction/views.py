# -*- coding: utf-8 -*-
import private_value_auction.forms as forms
from private_value_auction._builtin import Page, SubsessionWaitPage


class Introduction(Page):

    template_name = 'private_value_auction/Introduction.html'


class Bid(Page):

    template_name = 'private_value_auction/Bid.html'

    def get_form_class(self):
        return forms.BidForm


class ResultsWaitPage(SubsessionWaitPage):

    def after_all_players_arrive(self):
        self.subsession.set_payoffs()
        for p in self.subsession.players:
            p.set_payoff()


class Results(Page):

    template_name = 'private_value_auction/Results.html'

    def variables_for_template(self):
        return {'payoff': self.player.payoff,
                'bid_amount': self.player.bid_amount,
                'is_winner': self.player.is_winner}


def pages():

    return [Introduction,
            Bid,
            ResultsWaitPage,
            Results]