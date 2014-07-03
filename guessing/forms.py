# -*- coding: utf-8 -*-
import guessing.models as models
from guessing.utilities import ParticipantMixin
import ptree.forms


class GuessForm(ParticipantMixin, ptree.forms.Form):

    class Meta:
        model = models.Participant
        fields = ['guess_value']

    def labels(self):
        return {'guess_value': "What's your Guess?"}
