from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants
import random

class PlayerBot(Bot):
    """Bot that plays one round"""

    def play_round(self):
        yield (views.Contribute, {'contribution': c(1)})
        yield (views.Results)

