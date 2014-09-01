# -*- coding: utf-8 -*-
import cournot_competition.models as models
from cournot_competition._builtin import Form
import otree.forms
from django import forms

class UnitsForm(Form):

    class Meta:
        model = models.Player
        fields = ['units']
        widgets = {'units': forms.Select()}

    def labels(self):
        return {'units': 'How many units would you like to produce?'}

    def choices(self):
        # what if every player donates the max, then the price would be 0.
        # should 0 be an allowed production?
        return {'units': range(1, self.treatment.max_units_per_player()+1)}