# -*- coding: utf-8 -*-
import guessing.models as models
from guessing._builtin import Form


class GuessForm(Form):

    class Meta:
        model = models.Player
        fields = ['guess_value']

    def labels(self):
        return {'guess_value': "Pick a number:"}

    def guess_value_error_message(self, value):
        if not 0 <= value <= 100:
            return 'The value must be a whole number between {} and {}, inclusive.'.format(0, 100)
