# -*- coding: utf-8 -*-
import traveler_dilemma.models as models
from traveler_dilemma.utilities import ParticipantMixIn, MatchMixIn
import ptree.forms


class ClaimForm(ParticipantMixIn, ptree.forms.Form):

    class Meta:
        model = models.Participant
        fields = ['claim']

    def labels(self):
        return {'claim': "What's your Claim Amount?"}

    def choices(self):
        return {'claim': self.match.get_claim_field_choices()}

