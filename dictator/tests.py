from otree.api import Currency as c, currency_range, expect, Bot
from . import *


class PlayerBot(Bot):
    def play_round(self):
        yield Introduction

        if self.player.id_in_group == 1:
            yield Offer, dict(kept=cu(99))
            expect(self.player.payoff, cu(99))
        else:
            expect(self.player.payoff, cu(1))
        yield Results
