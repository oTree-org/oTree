# -*- coding: utf-8 -*-
import matrix_symmetric.models as models
from matrix_symmetric._builtin import Form
import otree.forms
from django import forms


class DecisionForm(Form):

    class Meta:
        model = models.Player
        fields = ['decision']
        widgets = {'decision': forms.RadioSelect()}

    def labels(self):
        return {'decision': 'Make a choice: Either A or B'}
