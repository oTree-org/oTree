# -*- coding: utf-8 -*-
import battle_of_the_sexes.models as models
from django import forms
from battle_of_the_sexes.utilities import ParticipantMixIn, MatchMixIn
import ptree.forms


class DecisionForm(ParticipantMixIn, ptree.forms.Form):

    class Meta:
        model = models.Participant
        fields = ['decision']
        widgets = {'decision': forms.RadioSelect()}

    def labels(self):
        return {'decision': 'Your Decision?'}
