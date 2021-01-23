from otree.api import Currency as c, currency_range, expect
from . import app
from otree.api import Bot
from .app import Constants


class PlayerBot(Bot):

    cases = [
        'success',  # players agree on an amount under the threshold
        'greedy',  # players ask for too much so end up with nothing
    ]

    def play_round(self):

        # start
        yield app.Introduction

        if self.case == 'success':
            request = c(10)
            yield app.Request, dict(request=request)
            yield app.Results
            expect(self.player.payoff, request)

        if self.case == 'greedy':
            yield app.Request, dict(request=Constants.amount_shared)
            yield app.Results
            expect(self.player.payoff, 0)
