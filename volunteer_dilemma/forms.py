# -*- coding: utf-8 -*-
import volunteer_dilemma.models as models
from django import forms
from volunteer_dilemma.utilities import Form
import ptree.forms


class DecisionForm(Form):

    class Meta:
        model = models.Participant
        fields = ['decision']
        widgets = {'decision': forms.RadioSelect()}

    def labels(self):
        return {'decision': 'Volunteer or Ignore?'}

