from otree.api import Currency as c, currency_range, expect
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        # compete price
        yield pages.Introduction
        yield pages.Decide, dict(price=c(30))
        yield pages.Results
