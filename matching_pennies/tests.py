from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants

class PlayerBot(Bot):

    def play_round(self):
        yield (pages.Choice, {"penny_side": 'Heads'})
        if self.player.role() == 'Matcher':
            assert self.player.is_winner
        else:
            assert not self.player.is_winner

        if self.player.round_number == Constants.num_rounds:
            # only 1 person should be paid in only 1 round
            total_payoffs = 0
            for player in self.group.get_players():
                total_payoffs += sum(p.payoff for p in player.in_all_rounds())
            assert total_payoffs == Constants.stakes
