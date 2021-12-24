from otree.api import Currency as c, currency_range, expect, Bot
from . import *


class PlayerBot(Bot):
    def play_round(self):
        yield Introduction
        yield Decision, dict(cooperate=True)
        expect('Both of you chose to Cooperate', 'in', self.html)
        expect(self.player.payoff, C.PAYOFF_B)
        yield Results
