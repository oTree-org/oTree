# -*- coding: utf-8 -*-
import travelers_dilemma.models as models
from travelers_dilemma.utilities import ParticipantMixin
import ptree.forms


class ClaimForm(ParticipantMixin, ptree.forms.Form):

    class Meta:
        model = models.Participant
        fields = ['claim']

    def labels(self):
        return {'claim': "What's your Claim Amount?"}

    def choices(self):
        return {'claim': self.match.get_claim_field_choices()}

