# -*- coding: utf-8 -*-
import bertand_competition.models as models
from bertand_competition.utilities import ParticipantMixIn
import ptree.forms


class PriceForm(ParticipantMixIn, ptree.forms.Form):

    class Meta:
        model = models.Participant
        fields = ['price']

    def labels(self):
        return {'price': 'Enter your preferred price?'}

    def price_error_message(self, value):
        if (value <= self.treatment.minimum_price) or (value > self.treatment.maximum_price):
            return 'Price should be between {} and {}'.format(self.treatment.minimum_price+1, self.treatment.maximum_price)