from otree.api import Currency as c, currency_range, SubmissionMustFail, expect
from . import app
from otree.api import Bot
from .app import Constants


class PlayerBot(Bot):
    cases = ['p1_wins', 'p1_and_p2_win']

    def play_round(self):
        if self.round_number == 1:
            yield app.Introduction

        if self.case == 'p1_wins':
            if self.player.id_in_group == 1:
                for invalid_guess in [-1, 101]:
                    yield SubmissionMustFail(app.Guess, dict(guess=invalid_guess))
                yield app.Guess, dict(guess=9)
                expect(self.player.payoff, Constants.jackpot)
                expect('you win', 'in', self.html)
            else:
                yield app.Guess, dict(guess=10)
                expect(self.player.payoff, 0)
                expect('you did not win', 'in', self.html)
        else:
            if self.player.id_in_group in [1, 2]:
                yield app.Guess, dict(guess=9)
                expect(self.player.payoff, Constants.jackpot / 2)
                expect('you are one of the 2 winners', 'in', self.html)
            else:
                yield app.Guess, dict(guess=10)
                expect(self.player.payoff, 0)
                expect('you did not win', 'in', self.html)

        yield app.Results
