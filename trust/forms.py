# -*- coding: utf-8 -*-
import trust.models as models
from trust.utilities import Form
from django import forms


class SendForm(Form):

    class Meta:
        model = models.Match
        fields = ['sent_amount']
        widgets = {'sent_amount': forms.RadioSelect()}

    def choices(self):
        return {'sent_amount': self.match.send_choices()}

    def labels(self):
        return {'sent_amount': "How much would you like to give?"}


class SendBackForm(Form):

    class Meta:
        model = models.Match
        fields = ['sent_back_amount']

    def choices(self):
        return {'sent_back_amount': self.match.send_back_choices()}

    def labels(self):
        return {'sent_back_amount': "How much would you like to give?"}
