from otree.api import Currency as c, currency_range, expect, Bot
from . import *


class PlayerBot(Bot):
    def play_round(self):
        yield Introduction
        yield Decision, dict(decision='Cooperate')
        expect('Both of you chose to Cooperate', 'in', self.html)
        expect(self.player.payoff, Constants.both_cooperate_payoff)
        yield Results
