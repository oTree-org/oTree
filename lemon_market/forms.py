# -*- coding: utf-8 -*-
import lemon_market.models as models
from lemon_market._builtin import Form


class BidForm(Form):

    class Meta:
        model = models.Match
        fields = ['bid_amount']

    def labels(self):
        #FIXME: this method has the wrong name? labels also defined below
        return {
            'bid_amount': self.match.bid_amount,
        }

    def labels(self):
        return {'bid_amount': 'Bid Amount'}

    def bid_amount_error_message(self, value):
        if not 0 <= value <= self.treatment.max_bid_amount:
            return 'Bid Amount should be between {} and {}'.format(0, self.treatment.max_bid_amount)

