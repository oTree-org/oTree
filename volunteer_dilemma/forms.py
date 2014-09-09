# -*- coding: utf-8 -*-
import volunteer_dilemma.models as models
from django import forms
from volunteer_dilemma._builtin import Form


class DecisionForm(Form):

    class Meta:
        model = models.Player
        fields = ['volunteer']
        widgets = {'volunteer': forms.RadioSelect()}

    def labels(self):
        return {'volunteer': 'Do you wish to volunteer?'}
