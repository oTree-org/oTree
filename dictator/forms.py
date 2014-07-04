# -*- coding: utf-8 -*-
import dictator.models as models
from django import forms
from django.forms import ValidationError
from dictator.utilities import ParticipantMixIn, ExperimenterMixIn
from django.utils.translation import ugettext_lazy as _
import ptree.forms
from crispy_forms.layout import HTML


class OfferForm(ParticipantMixIn, ptree.forms.Form):

    class Meta:
        model = models.Match
        fields = ['offer_amount']

    def labels(self):
        return {'offer_amount': 'How much will you offer?'}

    def choices(self):
        return {'offer_amount': self.match.get_offer_field_choices()}
