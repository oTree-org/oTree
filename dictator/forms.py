# -*- coding: utf-8 -*-
import dictator.models as models
from dictator.utilities import Form
import ptree.forms


class OfferForm(Form):

    class Meta:
        model = models.Match
        fields = ['offer_amount']

    def labels(self):
        return {'offer_amount': 'How much will you offer?'}

    def choices(self):
        return {'offer_amount': self.match.offer_choices()}
