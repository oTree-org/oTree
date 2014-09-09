# -*- coding: utf-8 -*-
import bertrand_competition.models as models
from bertrand_competition._builtin import Form


class PriceForm(Form):

    class Meta:
        model = models.Player
        fields = ['price']

    def labels(self):
        return {'price': "Choose a price for your firm's product:"}

    def price_error_message(self, value):
        if not self.treatment.marginal_cost < value <= self.treatment.maximum_price:
            return "The chosen price must be higher than {} and at most {}".format(self.treatment.marginal_cost, self.treatment.maximum_price)
