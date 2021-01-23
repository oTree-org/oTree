from otree.api import Currency as c, currency_range, expect
from . import app
from otree.api import Bot
from .app import Constants


class PlayerBot(Bot):

    cases = ['min', 'max']

    def play_round(self):
        yield app.Introduction

        if self.case == 'min':
            yield app.Decide, dict(units=0)
            # if player produces 0, nothing is sold and they make 0
            expect(self.player.payoff, c(0))

        if self.case == 'max':
            yield app.Decide, dict(units=Constants.max_units_per_player)
            # if everyone produces max, price is driven to 0
            expect(self.player.payoff, c(0))

        yield app.Results
