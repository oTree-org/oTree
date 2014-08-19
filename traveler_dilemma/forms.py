# -*- coding: utf-8 -*-
import traveler_dilemma.models as models
from traveler_dilemma._builtin import Form
import otree.forms


class ClaimForm(Form):

    class Meta:
        model = models.Player
        fields = ['claim']

    def labels(self):
        return {'claim': "What's your Claim Amount?"}

    def choices(self):
        return {'claim': self.match.claim_choices()}

