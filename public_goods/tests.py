from otree.api import Currency as c, currency_range, SubmissionMustFail, Submission, expect
from . import app
from otree.api import Bot
from .app import Constants


class PlayerBot(Bot):

    cases = ['basic', 'min', 'max']

    def play_round(self):
        case = self.case
        yield app.Introduction

        if case == 'basic':
            if self.player.id_in_group == 1:
                for invalid_contribution in [-1, 101]:
                    yield SubmissionMustFail(
                        app.Contribute, dict(contribution=invalid_contribution)
                    )

        contribution = dict(min=0, max=100, basic=50)[case]

        yield app.Contribute, dict(contribution=contribution)

        yield app.Results

        if self.player.id_in_group == 1:

            if case == 'min':
                expected_payoff = 100
            elif case == 'max':
                expected_payoff = 200
            else:
                expected_payoff = 150
            expect(self.player.payoff, expected_payoff)
