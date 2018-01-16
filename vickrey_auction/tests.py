from otree.api import Currency as c, currency_range, SubmissionMustFail
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    cases = ['p1_wins', 'all_0', 'all_max']

    def play_round(self):
        case = self.case

        # Introduction
        yield (pages.Introduction)

        if case == 'p1_wins':
            if self.player.id_in_group == 1:
                bid_amount = 2
            else:
                bid_amount = 1
        elif case == 'all_0':
            bid_amount = 0
        else:  # case == 'all_max':
            bid_amount = Constants.endowment
        yield (pages.Bid, {"bid_amount": bid_amount})

        assert self.player.payoff >= 0

        if case == 'p1_wins':
            if self.player.id_in_group == 1:
                assert 'You won the auction' in self.html
            else:
                assert 'You did not win' in self.html

        # group-level assertions
        if self.player.id_in_group == 1:
            assert self.group.highest_bid >= self.group.second_highest_bid
            num_winners = sum(
                [1 for p in self.group.get_players() if p.is_winner])
            assert num_winners == 1

        yield (pages.Results)
