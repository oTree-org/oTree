# -*- coding: utf-8 -*-
import bargaining.models as models
from bargaining.utilities import Form
import ptree.forms


class RequestForm(Form):

    class Meta:
        model = models.Participant
        fields = ['request_amount']

    def labels(self):
        return {'request_amount': 'Make your request?'}

    def choices(self):
        return {'request_amount': self.match.request_choices()}
