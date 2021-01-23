from otree.api import Currency as c, currency_range, expect
from . import app
from otree.api import Bot
from .app import Constants


class PlayerBot(Bot):
    cases = ['both_min', 'both_max', 'p1_lower']

    def play_round(self):
        case = self.case

        # start game
        yield app.Introduction

        if case == 'both_min':
            yield app.Claim, dict(claim=Constants.min_amount)
            expect(self.player.payoff, Constants.min_amount)
        elif case == 'both_max':
            yield app.Claim, dict(claim=Constants.max_amount)
            expect(self.player.payoff, Constants.max_amount)
        else:
            if self.player.id_in_group == 1:
                yield app.Claim, dict(claim=Constants.min_amount)
                expect(self.player.payoff, Constants.min_amount + 2)
            else:
                yield app.Claim, dict(claim=Constants.min_amount + 1)
                expect(self.player.payoff, Constants.min_amount - 2)

        yield app.Results
