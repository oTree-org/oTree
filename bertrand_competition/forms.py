# -*- coding: utf-8 -*-
import bertrand_competition.models as models
from bertrand_competition._builtin import Form
import otree.forms
from django import forms
from otree.common import Money, money_range


class PriceForm(Form):

    class Meta:
        model = models.Player
        fields = ['price']
        widgets = {'price': forms.Select()}

    def labels(self):
        return {'price': 'What price do you choose?'}

    def choices(self):
        # has to be above marginal cost, else they make no profit
        return {'price': money_range(self.treatment.marginal_cost+0.01, self.treatment.maximum_price)}
