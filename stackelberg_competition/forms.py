# -*- coding: utf-8 -*-
import stackelberg_competition.models as models
from stackelberg_competition._builtin import Form
import otree.forms


class QuantityForm(Form):

    class Meta:
        model = models.Player
        fields = ['quantity']

    def labels(self):
        return {'quantity': 'Enter the quantity of goods to produce?'}

    def quantity_error_message(self, value):
        lower_bound = 1
        upper_bound = self.treatment.total_capacity/2
        if not lower_bound <= value <= upper_bound:
            return 'Quantity should be between {} and {} units'.format(lower_bound, upper_bound)
