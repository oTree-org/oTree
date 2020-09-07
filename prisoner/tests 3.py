from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        yield (pages.Introduction)
        yield (pages.Decision, {"decision": 'Cooperate'})
        assert 'Both of you chose to Cooperate' in self.html
        assert self.player.payoff == Constants.both_cooperate_payoff
        yield (pages.Results)
