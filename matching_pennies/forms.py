# -*- coding: utf-8 -*-
import matching_pennies.models as models
from django import forms
from matching_pennies.utilities import Form
import otree.forms


class PennySideForm(Form):

    class Meta:
        model = models.Participant
        fields = ['penny_side']
        widgets = {'penny_side': forms.RadioSelect()}

    def labels(self):
        return {'penny_side': 'Please select a side:'}
