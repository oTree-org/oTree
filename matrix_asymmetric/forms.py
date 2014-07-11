# -*- coding: utf-8 -*-
import matrix_asymmetric.models as models
from matrix_asymmetric.utilities import ParticipantMixIn
import ptree.forms
from django import forms


class DecisionForm(ParticipantMixIn, ptree.forms.Form):

    class Meta:
        model = models.Participant
        fields = ['decision']
        widgets = {'decision': forms.RadioSelect()}

    def labels(self):
        return {'decision': 'Make a choice: Either A or B'}


