# -*- coding: utf-8 -*-
import trust.models as models
from trust.utilities import ParticipantMixin
import ptree.forms


class SendForm(ParticipantMixin, ptree.forms.Form):

    class Meta:
        model = models.Match
        fields = ['sent_amount']

    def choices(self):
        return {'sent_amount': self.match.get_send_field_choices()}

    def labels(self):
        return {'sent_amount': "How much would you like to give?"}


class SendBackForm(ParticipantMixin, ptree.forms.Form):

    class Meta:
        model = models.Match
        fields = ['sent_back_amount']

    def choices(self):
        return {'sent_back_amount': self.match.get_send_back_field_choices()}

    def labels(self):
        return {'sent_back_amount': "How much would you like to give?"}
