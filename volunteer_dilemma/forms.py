# -*- coding: utf-8 -*-
import volunteer_dilemma.models as models
from django import forms
from volunteer_dilemma.utilities import ParticipantMixIn, MatchMixIn
import ptree.forms


class DecisionForm(ParticipantMixIn, ptree.forms.Form):

    class Meta:
        model = models.Participant
        fields = ['decision']
        widgets = {'decision': forms.RadioSelect()}

    def labels(self):
        return {'decision': 'Volunteer or Ignore?'}

