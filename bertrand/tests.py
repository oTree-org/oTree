from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants

class PlayerBot(Bot):
    def play_round(self):
        # compete price
        yield (pages.Introduction)
        yield (pages.Decide, {'price': c(30)})
        yield (pages.Results)
