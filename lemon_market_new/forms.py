# -*- coding: utf-8 -*-
import lemon_market_new.models as models
from django import forms
from lemon_market_new._builtin import Form
from crispy_forms.layout import HTML
from otree.common import Money, money_range

class MyForm(Form):

    class Meta:
        model = models.Player
        fields = ['my_field']

    def my_field_error_message(self, value):
        if not 0 <= value <= 10:
            return 'Value is not in allowed range'

    def labels(self):
        return {}

    def order(self):
        pass
