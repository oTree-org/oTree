from otree.api import Currency as c, currency_range, expect, Bot
from . import *


class PlayerBot(Bot):
    cases = ['both_min', 'both_max', 'p1_lower']

    def play_round(self):
        case = self.case

        # start game
        yield Introduction

        if case == 'both_min':
            yield Claim, dict(claim=C.MIN_AMOUNT)
            expect(self.player.payoff, C.MIN_AMOUNT)
        elif case == 'both_max':
            yield Claim, dict(claim=C.MAX_AMOUNT)
            expect(self.player.payoff, C.MAX_AMOUNT)
        else:
            if self.player.id_in_group == 1:
                yield Claim, dict(claim=C.MIN_AMOUNT)
                expect(self.player.payoff, C.MIN_AMOUNT + 2)
            else:
                yield Claim, dict(claim=C.MIN_AMOUNT + 1)
                expect(self.player.payoff, C.MIN_AMOUNT - 2)

        yield Results
