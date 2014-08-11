# -*- coding: utf-8 -*-
import common_value_auction.models as models
from django import forms
from common_value_auction.utilities import Form
from crispy_forms.layout import HTML
from ptree.common import Money, money_range


class BidForm(Form):

    class Meta:
        model = models.Participant
        fields = ['bid_amount']

    def labels(self):
        return {'bid_amount': 'How much do you want to bid?'}

    def choices(self):
        return {'bid_amount': self.match.bid_choices()}
