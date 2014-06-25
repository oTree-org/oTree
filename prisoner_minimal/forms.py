# -*- coding: utf-8 -*-
import prisoner_minimal.models as models
from django import forms
from django.forms import ValidationError
from prisoner_minimal.utilities import ParticipantMixin, ExperimenterMixin
from django.utils.translation import ugettext_lazy as _
import ptree.forms
from crispy_forms.layout import HTML


class DecisionForm(ParticipantMixin, ptree.forms.Form):

    class Meta:
        model = models.Participant
        fields = ['decision']
        widgets = {'decision': forms.RadioSelect()}
