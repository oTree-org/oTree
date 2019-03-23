from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    cases = ['0_volunteer', '1_volunteer']

    def play_round(self):
        case = self.case

        yield (pages.Introduction)

        if case == '0_volunteer':
            yield (pages.Decision, {'volunteer': False})
            assert self.player.payoff == c(0)
            assert 'You did not volunteer and no one did' in self.html
        elif case == '1_volunteer':
            yield (pages.Decision, {'volunteer': self.player.id_in_group == 1})
            if self.player.id_in_group == 1:
                assert 'You volunteered' in self.html
                assert self.player.payoff == Constants.general_benefit - Constants.volunteer_cost
            else:
                assert 'You did not volunteer but some did' in self.html
                assert self.player.payoff == c(100)
        yield (pages.Results)
