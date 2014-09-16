# -*- coding: utf-8 -*-
import stag_hunt.models as models
from django import forms
from stag_hunt._builtin import Form


class DecisionForm(Form):

    class Meta:
        model = models.Player
        fields = ['decision']
        widgets = {'decision': forms.RadioSelect()}

    def labels(self):
        return {'decision': "Please make a choice:"}
