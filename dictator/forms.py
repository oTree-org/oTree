# -*- coding: utf-8 -*-
import dictator.models as models
from dictator._builtin import Form
from django import forms
from otree.common import Money, money_range


class OfferForm(Form):

    class Meta:
        model = models.Match
        fields = ['offer_amount']

    def labels(self):
        return {'offer_amount': 'How much will you offer?'}

    def choices(self):
        return {'offer_amount': money_range(0, self.treatment.allocated_amount, 0.05)}
