# -*- coding: utf-8 -*-
import prisoner_minimal.models as models
from django import forms
from prisoner_minimal.utilities import ParticipantMixin
import ptree.forms


class DecisionForm(ParticipantMixin, ptree.forms.Form):

    class Meta:
        model = models.Participant
        fields = ['decision']
        widgets = {'decision': forms.RadioSelect()}
