from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants

class PlayerBot(Bot):

    def play_round(self):

        yield (views.Introduction)

        if self.player.id_in_group == 1:
            yield (views.Send, {"sent_amount": 4})

        else:
            yield (views.SendBack, {'sent_back_amount': 8})

        yield (views.Results)
