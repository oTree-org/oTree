# -*- coding: utf-8 -*-
import private_value_auction.models as models
from private_value_auction._builtin import Form
from otree.common import Money


class BidForm(Form):

    class Meta:
        model = models.Player
        fields = ['bid_amount']

    def labels(self):
        return {'bid_amount': 'Bid amount:'}

    def bid_amount_error_message(self, value):
        if not self.treatment.min_allowable_bid <= value <= self.treatment.max_allowable_bid:
            return 'The amount bidded must be between {} and {}, inclusive.'.format(Money(self.treatment.min_allowable_bid), Money(self.treatment.max_allowable_bid))
