# -*- coding: utf-8 -*-
import coordination.models as models
from coordination.utilities import ParticipantMixIn
import ptree.forms
from django import forms


class ChoiceForm(ParticipantMixIn, ptree.forms.Form):

    class Meta:
        model = models.Participant
        fields = ['choice']
        widgets = {'choice': forms.RadioSelect()}

    def labels(self):
        return {'choice': 'Your Choice?'}
