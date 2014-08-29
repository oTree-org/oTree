# -*- coding: utf-8 -*-
import matrix_asymmetric.models as models
from matrix_asymmetric._builtin import Form
from django import forms


class DecisionForm(Form):

    class Meta:
        model = models.Player
        fields = ['decision']
        widgets = {'decision': forms.RadioSelect()}

    def labels(self):
        return {'decision': 'Make a choice:'}
