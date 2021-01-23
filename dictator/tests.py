from otree.api import Currency as c, currency_range, expect
from . import app
from otree.api import Bot
from .app import Constants


class PlayerBot(Bot):
    def play_round(self):
        yield app.Introduction

        if self.player.id_in_group == 1:
            yield app.Offer, dict(kept=c(99))
            expect(self.player.payoff, c(99))
        else:
            expect(self.player.payoff, c(1))
        yield app.Results
