from otree.api import Currency as c, currency_range, SubmissionMustFail
from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    cases = [
        {'offer': 0, 'return': 0, 'p1_payoff': 10, 'p2_payoff': 0},
        {'offer': 5, 'return': 10, 'p1_payoff': 15, 'p2_payoff': 5},
        {'offer': 10, 'return': 30, 'p1_payoff': 30, 'p2_payoff': 0}
    ]

    def play_round(self):
        case = self.case
        if self.player.id_in_group == 1:
            yield (views.Send, {"sent_amount": case['offer']})

        else:
            for invalid_return in [-1, case['offer'] * Constants.multiplication_factor + 1]:
                yield SubmissionMustFail(views.SendBack,
                                         {'sent_back_amount': invalid_return})
            yield (views.SendBack, {'sent_back_amount': case['return']})

        if self.player.id_in_group == 1:
            expected_payoff = case['p1_payoff']
        else:
            expected_payoff = case['p2_payoff']

        assert self.player.payoff == expected_payoff
