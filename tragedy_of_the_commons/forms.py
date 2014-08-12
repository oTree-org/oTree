# -*- coding: utf-8 -*-
import tragedy_of_the_commons.models as models
from django import forms
from tragedy_of_the_commons.utilities import Form
from crispy_forms.layout import HTML
from otree.common import Money, money_range


class DecisionForm(Form):

    class Meta:
        model = models.Player
        fields = ['decision']
        widgets = {'decision': forms.RadioSelect()}

    def labels(self):
        return {'decision': 'Your Decision?'}
