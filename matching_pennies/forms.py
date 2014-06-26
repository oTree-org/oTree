# -*- coding: utf-8 -*-
import matching_pennies.models as models
from django import forms
from django.forms import ValidationError
from matching_pennies.utilities import ParticipantMixin, ExperimenterMixin
from django.utils.translation import ugettext_lazy as _
import ptree.forms
from crispy_forms.layout import HTML


class PennySideForm(ParticipantMixin, ptree.forms.Form):

    class Meta:
        model = models.Participant
        fields = ['penny_side']
        widgets = {'penny_side': forms.RadioSelect()}

    def labels(self):
        return {'penny_side': 'Which penny side do you choose?'}

