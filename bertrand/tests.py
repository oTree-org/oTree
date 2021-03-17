from otree.api import Currency as c, currency_range, expect, Bot
from . import *


class PlayerBot(Bot):
    def play_round(self):
        # compete price
        yield Introduction
        yield Decide, dict(price=cu(30))
        yield Results
