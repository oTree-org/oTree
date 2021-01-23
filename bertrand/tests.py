from otree.api import Currency as c, currency_range, expect
from . import app
from otree.api import Bot
from .app import Constants


class PlayerBot(Bot):
    def play_round(self):
        # compete price
        yield app.Introduction
        yield app.Decide, dict(price=c(30))
        yield app.Results
