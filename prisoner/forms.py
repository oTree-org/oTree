# -*- coding: utf-8 -*-
import prisoner.models as models
from django import forms
from prisoner.utilities import Form


class DecisionForm(Form):

    class Meta:
        model = models.Player
        fields = ['decision']
        widgets = {'decision': forms.RadioSelect()}
