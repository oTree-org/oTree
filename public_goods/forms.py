# -*- coding: utf-8 -*-
import public_goods.models as models
from django import forms
from django.forms import ValidationError
from public_goods.utilities import ParticipantMixin, ExperimenterMixin
from django.utils.translation import ugettext_lazy as _
import ptree.forms
from crispy_forms.layout import HTML


class ContributeForm(ParticipantMixin, ptree.forms.Form):

    class Meta:
        model = models.Participant
        fields = ['contributed_amount']

    def labels(self):
        return {'contributed_amount': 'How much do you want to contribute to the group project?'}

    def choices(self):
        return {'contributed_amount': self.participant.get_contribute_choices()}
