from otree.api import Currency as c, currency_range, expect, Bot
from . import *


class PlayerBot(Bot):

    cases = ['min', 'max']

    def play_round(self):
        yield Introduction

        if self.case == 'min':
            yield Decide, dict(units=0)
            # if player produces 0, nothing is sold and they make 0
            expect(self.player.payoff, cu(0))

        if self.case == 'max':
            yield Decide, dict(units=Constants.max_units_per_player)
            # if everyone produces max, price is driven to 0
            expect(self.player.payoff, cu(0))

        yield Results
