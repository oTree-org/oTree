# -*- coding: utf-8 -*-
import cournot_competition.models as models
from cournot_competition._builtin import Form


class UnitsForm(Form):

    class Meta:
        model = models.Player
        fields = ['units']
        #widgets = {'units': forms.Select()}

    def labels(self):
        return {'units': 'How many units will you produce:'}

    def units_error_message(self, value):
        if not 0 <= value <= self.treatment.max_units_per_player():
            return "The value must be a whole number between {} and {}, inclusive.".format(0, self.treatment.max_units_per_player())
