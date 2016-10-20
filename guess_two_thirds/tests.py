from otree.api import Currency as c, currency_range, SubmissionMustFail
from . import views
from ._builtin import Bot
from .models import Constants

class PlayerBot(Bot):
    cases = ['p1_wins', 'p1_and_p2_win']

    def play_round(self):
        if self.subsession.round_number == 1:
            yield (views.Introduction)

        if self.case == 'p1_wins':
            if self.player.id_in_group == 1:
                for invalid_guess in [-1, 101]:
                    yield SubmissionMustFail(views.Guess, {"guess": invalid_guess})
                yield (views.Guess, {"guess": 9})
                assert self.player.payoff == Constants.jackpot
                assert 'you win' in self.html
            else:
                yield (views.Guess, {"guess": 10})
                assert self.player.payoff == 0
                assert 'you did not win' in self.html
        else:
            if self.player.id_in_group in [1, 2]:
                yield (views.Guess, {"guess": 9})
                assert self.player.payoff == Constants.jackpot / 2
                assert 'you are one of the 2 winners' in self.html
            else:
                yield (views.Guess, {"guess": 10})
                assert self.player.payoff == 0
                assert 'you did not win' in self.html

        yield (views.Results)
