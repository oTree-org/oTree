from otree.api import Currency as c, currency_range, expect
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    cases = ['both_min', 'both_max', 'p1_lower']

    def play_round(self):
        case = self.case

        # start game
        yield pages.Introduction

        if case == 'both_min':
            yield pages.Claim, dict(claim=Constants.min_amount)
            expect(self.player.payoff, Constants.min_amount)
        elif case == 'both_max':
            yield pages.Claim, dict(claim=Constants.max_amount)
            expect(self.player.payoff, Constants.max_amount)
        else:
            if self.player.id_in_group == 1:
                yield pages.Claim, dict(claim=Constants.min_amount)
                expect(self.player.payoff, Constants.min_amount + 2)
            else:
                yield pages.Claim, dict(claim=Constants.min_amount + 1)
                expect(self.player.payoff, Constants.min_amount - 2)

        yield pages.Results
