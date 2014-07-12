# -*- coding: utf-8 -*-
import ptree.views
import ptree.views.concrete
import private_value_auction.forms as forms
from private_value_auction.utilities import ParticipantMixIn, ExperimenterMixIn
from ptree.common import currency


class Introduction(ParticipantMixIn, ptree.views.Page):

    def show_skip_wait(self):
        return self.PageActions.show

    template_name = 'private_value_auction/Introduction.html'


class Bid(ParticipantMixIn, ptree.views.Page):

    def show_skip_wait(self):
        return self.PageActions.show

    template_name = 'private_value_auction/Bid.html'

    def get_form_class(self):
        return forms.BidForm

    def variables_for_template(self):
        return {
            'price_value': currency(self.treatment.price_value),
        }


class Results(ParticipantMixIn, ptree.views.Page):

    def show_skip_wait(self):
        if self.participant.other_participant().bid_amount:
            return self.PageActions.show
        else:
            return self.PageActions.wait

    template_name = 'private_value_auction/Results.html'

    def variables_for_template(self):
        if self.participant.payoff is None:
            self.participant.set_payoff()

        return {
            'payoff': currency(self.participant.payoff),
            'bid_amount': currency(self.participant.bid_amount),
            'is_winner': self.participant.is_winner
        }


class ExperimenterPage(ExperimenterMixIn, ptree.views.ExperimenterPage):
    pass


def pages():
    return [
        Introduction,
        Bid,
        Results
    ]