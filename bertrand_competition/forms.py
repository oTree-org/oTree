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
        lower = self.treatment.minimum_price+0.01
        upper = self.treatment.maximum_price
        if not lower <= value <= upper:
            return 'Price should be between {} and {}'.format(lower, upper)