from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    cases = [
        'success', # players agree on an amount under the threshold
        'greedy', # players ask for too much so end up with nothing
    ]

    def play_round(self):

        # start
        yield (views.Introduction)

        if self.case == 'success':
            request_amount = c(10)
            yield (views.Request, {"request_amount": request_amount})
            yield (views.Results)
            assert self.player.payoff == request_amount

        if self.case == 'greedy':
            yield (views.Request, {"request_amount": Constants.amount_shared})
            yield (views.Results)
            assert self.player.payoff == 0
