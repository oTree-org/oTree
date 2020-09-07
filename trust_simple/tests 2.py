from otree.api import Currency as c, currency_range, SubmissionMustFail, expect
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    cases = [
        {'offer': c(0), 'return': c(0), 'p1_payoff': c(10), 'p2_payoff': c(0)},
        {'offer': c(5), 'return': c(10), 'p1_payoff': c(15), 'p2_payoff': c(5)},
        {'offer': c(10), 'return': c(30), 'p1_payoff': c(30), 'p2_payoff': c(0)},
    ]

    def play_round(self):
        case = self.case
        if self.player.id_in_group == 1:
            yield pages.Send, dict(sent_amount=case['offer'])

        else:
            for invalid_return in [-1, case['offer'] * Constants.multiplier + 1]:
                yield SubmissionMustFail(
                    pages.SendBack, dict(sent_back_amount=invalid_return)
                )
            yield pages.SendBack, dict(sent_back_amount=case['return'])

        if self.player.id_in_group == 1:
            expected_payoff = case['p1_payoff']
        else:
            expected_payoff = case['p2_payoff']

        expect(self.player.payoff, expected_payoff)
