# -*- coding: utf-8 -*-
import bargaining.models as models
from bargaining._builtin import Form


class RequestForm(Form):

    class Meta:
        model = models.Player
        fields = ['request_amount']

    def labels(self):
        return {'request_amount': 'Amount requested:'}

    def choices(self):
        return {'request_amount': self.match.request_choices()}
