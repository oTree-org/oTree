from otree.api import Currency as c, currency_range, SubmissionMustFail
from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    cases = ['basic', 'tie']

    def play_round(self):
        case = self.case

        yield (views.Introduction)

        if case == 'basic':
            if self.player.id_in_group == 1:
                for invalid_guess in [-1, 101]:
                    yield SubmissionMustFail(views.Guess,
                                             {"guess_value": invalid_guess})
            if self.player.id_in_group == 2:
                yield (views.Guess, {"guess_value": 9})
                assert self.player.is_winner
                assert 'you were the winner' in self.html
            else:
                yield (views.Guess, {"guess_value": 10})
                assert not self.player.is_winner
                assert 'you were not the winner' in self.html
            expected_winners = 1
        else:
            if self.player.id_in_group in [2, 4]:
                yield (views.Guess, {"guess_value": 9})
                assert self.player.is_winner
                assert 'you were one of them' in self.html
            else:
                yield (views.Guess, {"guess_value": 10})
                assert not self.player.is_winner
                assert 'you were not one of them' in self.html
            expected_winners = 2

        if self.player.id_in_group == 1:
            num_winners = sum(
                [1 for p in self.group.get_players() if p.is_winner])
            assert num_winners == expected_winners
            if num_winners > 1:
                assert self.group.tie == True

        yield (views.Results)
