# -*- coding: utf-8 -*-
import tragedy_of_the_commons.models as models
from django import forms
from tragedy_of_the_commons._builtin import Form
from crispy_forms.layout import HTML
from otree.common import Money, money_range


class DecideForm(Form):

    class Meta:
        model = models.Player
        fields = ['hours_fished']

    def hours_fished_error_message(self, value):
        if not 0 <= value <= 10:
            return 'The value must be a whole number between {} and {}, inclusive.'.format(0, 10)

    def labels(self):
        return {'hours_fished': 'How many hours do you want to fish?'}
