# -*- coding: utf-8 -*-
import matrix_asymmetric.models as models
from matrix_asymmetric.utilities import Form
import otree.forms
from django import forms


class DecisionForm(Form):

    class Meta:
        model = models.Participant
        fields = ['decision']
        widgets = {'decision': forms.RadioSelect()}

    def labels(self):
        return {'decision': 'Make a choice: Either A or B'}


