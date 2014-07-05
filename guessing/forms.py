# -*- coding: utf-8 -*-
import guessing.models as models
from guessing.utilities import ParticipantMixIn
import ptree.forms


class GuessForm(ParticipantMixIn, ptree.forms.Form):

    class Meta:
        model = models.Participant
        fields = ['guess_value']

    def labels(self):
        return {'guess_value': "What's your Guess?"}
