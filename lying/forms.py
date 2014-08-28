# -*- coding: utf-8 -*-
import lying.models as models
from lying._builtin import Form


class CoinFlipForm(Form):

    class Meta:
        model = models.Player
        fields = ['number_of_heads']

    def choices(self):
        return {'number_of_heads': range(0, self.treatment.number_of_flips + 1)}

    def labels(self):
        return {'number_of_heads': 'Number of heads:'}
