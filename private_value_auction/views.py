# -*- coding: utf-8 -*-
import ptree.views
import ptree.views.concrete
import private_value_auction.forms as forms
from private_value_auction.utilities import ParticipantMixIn, MatchMixIn, SubsessionMixIn
from ptree.common import currency


class Introduction(ParticipantMixIn, ptree.views.Page):

    template_name = 'private_value_auction/Introduction.html'


class Bid(ParticipantMixIn, ptree.views.Page):

    template_name = 'private_value_auction/Bid.html'

    def get_form_class(self):
        return forms.BidForm

    def variables_for_template(self):
        return {
            'price_value': currency(self.treatment.price_value),
        }

class ResultsCheckpoint(MatchMixIn, ptree.views.MatchCheckpoint):

    def action(self):
        for p in self.subsession.participants():
            p.set_payoff()


class Results(ParticipantMixIn, ptree.views.Page):

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
        ResultsCheckpoint,
        Results
    ]