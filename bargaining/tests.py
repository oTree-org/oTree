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
            request_amount = c(10)
            yield (pages.Request, {"request_amount": request_amount})
            yield (pages.Results)
            assert self.player.payoff == request_amount

        if self.case == 'greedy':
            yield (pages.Request, {"request_amount": Constants.amount_shared})
            yield (pages.Results)
            assert self.player.payoff == 0
