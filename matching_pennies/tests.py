from otree.api import Currency as c, currency_range, expect
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        yield pages.Choice, dict(penny_side='Heads')
        if self.player.is_matcher():
            expect(self.player.is_winner, True)
        else:
            expect(self.player.is_winner, False)

        if self.player.round_number == Constants.num_rounds:
            # only 1 person should be paid in only 1 round
            total_payoffs = 0
            for player in self.group.get_players():
                total_payoffs += sum(p.payoff for p in player.in_all_rounds())
            expect(total_payoffs, Constants.stakes)
