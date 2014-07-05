# -*- coding: utf-8 -*-
import prisoner.models as models
from django import forms
from prisoner.utilities import ParticipantMixIn
import ptree.forms


class DecisionForm(ParticipantMixIn, ptree.forms.Form):

    class Meta:
        model = models.Participant
        fields = ['decision']
        widgets = {'decision': forms.RadioSelect()}
