import lying.models as models
import otree.forms
from lying._builtin import Form
from otree.common import Money, money_range
from decimal import Decimal

class CoinFlipForm(Form):

    class Meta:
        model = models.Player
        fields = ['number_of_heads']

    def number_of_heads_error_message(self, value):
        if (value > self.treatment.number_of_flips):
            return 'Number of heads cannot be more than {}'.format(self.treatment.number_of_flips)

    def choices(self):
        return {
            'number_of_heads': range(0, self.treatment.number_of_flips + 1),
        }