# -*- coding: utf-8 -*-
import stag_hunt.models as models
from django import forms
from stag_hunt.utilities import Form
import otree.forms


class DecisionForm(Form):

    class Meta:
        model = models.Participant
        fields = ['decision']
        widgets = {'decision': forms.RadioSelect()}

    def labels(self):
        return {'decision': 'Your Decision?'}
