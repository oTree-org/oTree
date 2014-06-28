# -*- coding: utf-8 -*-
import travelers_dilemma.models as models
from travelers_dilemma.utilities import ParticipantMixin
import ptree.forms


class EstimateValueForm(ParticipantMixin, ptree.forms.Form):

    class Meta:
        model = models.Participant
        fields = ['estimate_value']

    def labels(self):
        return {'estimate_value': "What's the estimated value of your items?"}

    def choices(self):
        return {'estimate_value': self.match.get_value_field_choices()}

