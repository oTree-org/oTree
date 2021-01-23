from otree.api import Currency as c, currency_range, expect
from . import app
from otree.api import Bot
from .app import Constants


class PlayerBot(Bot):
    def play_round(self):
        yield app.Introduction
        yield app.Decision, dict(decision='Cooperate')
        expect('Both of you chose to Cooperate', 'in', self.html)
        expect(self.player.payoff, Constants.both_cooperate_payoff)
        yield app.Results
