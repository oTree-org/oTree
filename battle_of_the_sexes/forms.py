# -*- coding: utf-8 -*-
import battle_of_the_sexes.models as models
from django import forms
from battle_of_the_sexes._builtin import Form
import otree.forms


class DecisionForm(Form):

    class Meta:
        model = models.Player
        fields = ['decision']
        widgets = {'decision': forms.RadioSelect()}

    def labels(self):
        return {'decision': 'Your Decision?'}
