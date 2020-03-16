from otree.api import Currency as c, currency_range, expect
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        yield pages.Introduction

        if self.player.id_in_group == 1:
            yield pages.Offer, dict(kept=c(99))
            expect(self.player.payoff, c(99))
        else:
            expect(self.player.payoff, c(1))
        yield pages.Results
