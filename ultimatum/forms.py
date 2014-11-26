# -*- coding: utf-8 -*-
import ultimatum.models as models
from django import forms
from ultimatum.utilities import PlayerMixin
from django.utils.translation import ugettext_lazy as _, ugettext
import otree.forms
from otree.common import currency


invalid_amount_string = _('Not an allowed amount')


class OfferForm(PlayerMixin, otree.forms.Form):

    class Meta:
        model = models.Match
        fields = ['amount_offered']

    def choices(self):
        return {'amount_offered': self.match.get_field_choices_tuples()}

    def labels(self):
        return {'amount_offered': _("How much would you like to offer?")}


class AcceptForm(PlayerMixin, otree.forms.Form):

    class Meta:
        model = models.Match
        fields = ['offer_accepted']

    def labels(self):
        return {'offer_accepted': _("Do you wish to accept the offer?")}


