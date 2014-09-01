# -*- coding: utf-8 -*-
import stackelberg_competition.models as models
from stackelberg_competition._builtin import Form


class QuantityForm(Form):

    class Meta:
        model = models.Player
        fields = ['quantity']

    def labels(self):
        return {'quantity': 'How many units will you produce:'}

    def quantity_error_message(self, value):
        if not 0 <= value <= self.treatment.max_units_per_player():
            return "The value must be a whole number between {} and {}, inclusive.".format(0, self.treatment.max_units_per_player())
