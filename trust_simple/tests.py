from otree.api import Currency as c, currency_range, expect, Bot, SubmissionMustFail
from . import *


class PlayerBot(Bot):
    cases = [
        {'offer': cu(0), 'return': cu(0), 'p1_payoff': cu(10), 'p2_payoff': cu(0)},
        {'offer': cu(5), 'return': cu(10), 'p1_payoff': cu(15), 'p2_payoff': cu(5)},
        {'offer': cu(10), 'return': cu(30), 'p1_payoff': cu(30), 'p2_payoff': cu(0)},
    ]

    def play_round(self):
        case = self.case
        if self.player.id_in_group == 1:
            yield Send, dict(sent_amount=case['offer'])

        else:
            for invalid_return in [-1, case['offer'] * Constants.multiplier + 1]:
                yield SubmissionMustFail(
                    SendBack, dict(sent_back_amount=invalid_return)
                )
            yield SendBack, dict(sent_back_amount=case['return'])

        if self.player.id_in_group == 1:
            expected_payoff = case['p1_payoff']
        else:
            expected_payoff = case['p2_payoff']

        expect(self.player.payoff, expected_payoff)
