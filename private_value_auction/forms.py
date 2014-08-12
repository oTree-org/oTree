# -*- coding: utf-8 -*-
import private_value_auction.models as models
from private_value_auction.utilities import Form
import otree.forms


class BidForm(Form):

    class Meta:
        model = models.Player
        fields = ['bid_amount']

    def choices(self):
        return {'bid_amount': self.match.bid_choices()}

    def labels(self):
        return {'bid_amount': 'Your Bid Amount?'}
