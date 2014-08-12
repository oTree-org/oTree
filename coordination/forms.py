# -*- coding: utf-8 -*-
import coordination.models as models
from coordination.utilities import Form
import otree.forms
from django import forms


class ChoiceForm(Form):

    class Meta:
        model = models.Player
        fields = ['choice']
        widgets = {'choice': forms.RadioSelect()}

    def labels(self):
        return {'choice': 'Your Choice?'}
