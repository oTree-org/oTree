from otree.api import Currency as c, currency_range, expect, Bot
from . import *


class PlayerBot(Bot):
    cases = ['both_min', 'both_max', 'p1_lower']

    def play_round(self):
        case = self.case

        # start game
        yield Introduction

        if case == 'both_min':
            yield Claim, dict(claim=Constants.min_amount)
            expect(self.player.payoff, Constants.min_amount)
        elif case == 'both_max':
            yield Claim, dict(claim=Constants.max_amount)
            expect(self.player.payoff, Constants.max_amount)
        else:
            if self.player.id_in_group == 1:
                yield Claim, dict(claim=Constants.min_amount)
                expect(self.player.payoff, Constants.min_amount + 2)
            else:
                yield Claim, dict(claim=Constants.min_amount + 1)
                expect(self.player.payoff, Constants.min_amount - 2)

        yield Results
