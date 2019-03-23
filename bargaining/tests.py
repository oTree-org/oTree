from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    cases = [
        'success', # players agree on an amount under the threshold
        'greedy', # players ask for too much so end up with nothing
    ]

    def play_round(self):

        # start
        yield (pages.Introduction)

        if self.case == 'success':
            request = c(10)
            yield (pages.Request, {"request": request})
            yield (pages.Results)
            assert self.player.payoff == request

        if self.case == 'greedy':
            yield (pages.Request, {"request": Constants.amount_shared})
            yield (pages.Results)
            assert self.player.payoff == 0
