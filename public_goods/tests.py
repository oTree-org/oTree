from otree.api import Currency as c, currency_range, expect, Bot, SubmissionMustFail
from . import *


class PlayerBot(Bot):

    cases = ['basic', 'min', 'max']

    def play_round(self):
        case = self.case
        yield Introduction

        if case == 'basic':
            if self.player.id_in_group == 1:
                for invalid_contribution in [-1, 101]:
                    yield SubmissionMustFail(
                        Contribute, dict(contribution=invalid_contribution)
                    )

        contribution = dict(min=0, max=100, basic=50)[case]

        yield Contribute, dict(contribution=contribution)

        yield Results

        if self.player.id_in_group == 1:

            if case == 'min':
                expected_payoff = 100
            elif case == 'max':
                expected_payoff = 200
            else:
                expected_payoff = 150
            expect(self.player.payoff, expected_payoff)
