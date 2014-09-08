# -*- coding: utf-8 -*-
import volunteer_dilemma.models as models
from django import forms
from volunteer_dilemma._builtin import Form


class DecisionForm(Form):

    class Meta:
        model = models.Player
        fields = ['decision']
        widgets = {'decision': forms.RadioSelect()}

    def labels(self):
        return {'decision': 'Volunteer or Ignore?'}

