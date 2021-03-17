from otree.api import Currency as c, currency_range, expect, Bot
from . import *


class PlayerBot(Bot):

    cases = [
        'success',  # players agree on an amount under the threshold
        'greedy',  # players ask for too much so end up with nothing
    ]

    def play_round(self):

        # start
        yield Introduction

        if self.case == 'success':
            request = cu(10)
            yield Request, dict(request=request)
            yield Results
            expect(self.player.payoff, request)

        if self.case == 'greedy':
            yield Request, dict(request=Constants.amount_shared)
            yield Results
            expect(self.player.payoff, 0)
