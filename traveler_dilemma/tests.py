from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants

class PlayerBot(Bot):
    cases = [
        'both_min',
        'both_max',
        'p1_lower'
    ]

    def play_round(self):
        case = self.case

        # start game
        yield (pages.Introduction)

        if case == 'both_min':
            yield (pages.Claim, {"claim": Constants.min_amount})
            assert self.player.payoff == Constants.min_amount
        elif case == 'both_max':
            yield (pages.Claim, {"claim": Constants.max_amount})
            assert self.player.payoff == Constants.max_amount
        else:
            if self.player.id_in_group == 1:
                yield (pages.Claim, {"claim": Constants.min_amount})
                assert self.player.payoff == Constants.min_amount + 2
            else:
                yield (pages.Claim, {"claim": Constants.min_amount + 1})
                assert self.player.payoff == Constants.min_amount - 2

        yield (pages.Results)
