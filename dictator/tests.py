from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants

class PlayerBot(Bot):
    def play_round(self):
        yield (pages.Introduction)

        if self.player.id_in_group == 1:
            yield (pages.Offer, {"kept": c(99)})
            assert self.player.payoff == c(99)
        else:
            assert self.player.payoff == c(1)
        yield (pages.Results)
