from otree.api import Currency as c, currency_range, expect
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        yield pages.Introduction
        yield pages.Decision, dict(decision='Cooperate')
        expect('Both of you chose to Cooperate', 'in', self.html)
        expect(self.player.payoff, Constants.both_cooperate_payoff)
        yield pages.Results
