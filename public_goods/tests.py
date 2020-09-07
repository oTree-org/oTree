from otree.api import (
    Currency as c, currency_range, SubmissionMustFail, Submission
)
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    cases = ['basic', 'min', 'max']

    def play_round(self):
        case = self.case
        yield (pages.Introduction)

        if case == 'basic':
            if self.player.id_in_group == 1:
                for invalid_contribution in [-1, 101]:
                    yield SubmissionMustFail(pages.Contribute, {
                        'contribution': invalid_contribution})

        contribution = {
            'min': 0,
            'max': 100,
            'basic': 50,
        }[case]

        yield (pages.Contribute, {"contribution": contribution})

        yield (pages.Results)

        if self.player.id_in_group == 1:

            if case == 'min':
                expected_payoff = 100
            elif case == 'max':
                expected_payoff = 200
            else:
                expected_payoff = 150
            assert self.player.payoff == expected_payoff
