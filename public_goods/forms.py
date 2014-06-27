# -*- coding: utf-8 -*-
import public_goods.models as models
from public_goods.utilities import ParticipantMixin
import ptree.forms


class ContributeForm(ParticipantMixin, ptree.forms.Form):

    class Meta:
        model = models.Participant
        fields = ['contributed_amount']

    def labels(self):
        return {'contributed_amount': 'How much do you want to contribute to the group project?'}

    def choices(self):
        return {'contributed_amount': self.participant.get_contribute_choices()}
