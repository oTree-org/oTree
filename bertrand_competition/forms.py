# -*- coding: utf-8 -*-
import bertrand_competition.models as models
from bertrand_competition._builtin import Form
import otree.forms


class PriceForm(Form):

    class Meta:
        model = models.Player
        fields = ['price']

    def labels(self):
        return {'price': 'Enter your preferred price?'}

    def price_error_message(self, value):
        if not self.treatment.minimum_price < value <= self.treatment.maximum_price:
            return 'Price should be between {} and {}'.format(self.treatment.minimum_price+0.01, self.treatment.maximum_price)