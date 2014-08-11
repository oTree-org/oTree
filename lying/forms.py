import lying.models as models
import ptree.forms
from lying.utilities import Form
from ptree.common import Money, money_range
from decimal import Decimal

class CoinFlipForm(Form):

    class Meta:
        model = models.Participant
        fields = ['number_of_heads']

    def number_of_heads_error_message(self, value):
        if (value > self.treatment.number_of_flips):
            return 'Number of heads cannot be more than {}'.format(self.treatment.number_of_flips)

    def choices(self):
        return {
            'number_of_heads': range(0, self.treatment.number_of_flips + 1),
        }