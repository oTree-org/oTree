# -*- coding: utf-8 -*-
import public_goods.models as models
from public_goods._builtin import Form


class ContributeForm(Form):

    class Meta:
        model = models.Player
        fields = ['contribution']

    def labels(self):
        return {'contribution': 'How much do you want to contribute to the group project?'}

    def choices(self):
        return {'contribution': self.treatment.contribute_choices()}
