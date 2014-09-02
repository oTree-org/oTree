# -*- coding: utf-8 -*-
import common_value_auction.models as models
from common_value_auction._builtin import Form
from otree.common import Money


class BidForm(Form):

    class Meta:
        model = models.Player
        fields = ['bid_amount']

    def labels(self):
        return {'bid_amount': 'Bid amount:'}

    def bid_amount_error_message(self, value):
        if not self.treatment.item_value_min <= value <= self.treatment.item_value_max:
            return 'The amount bidded must be between {} and {}, inclusive.'.format(Money(self.treatment.item_value_min), Money(self.treatment.item_value_max))
