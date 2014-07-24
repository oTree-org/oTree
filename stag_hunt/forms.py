# -*- coding: utf-8 -*-
import stag_hunt.models as models
from django import forms
from stag_hunt.utilities import ParticipantMixIn
import ptree.forms


class DecisionForm(ParticipantMixIn, ptree.forms.Form):

    class Meta:
        model = models.Participant
        fields = ['decision']
        widgets = {'decision': forms.RadioSelect()}

    def labels(self):
        return {'decision': 'Your Decision?'}
