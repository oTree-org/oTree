from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants

class PlayerBot(Bot):
    cases = [
        {
            'p1_quantity': 0,
            'p2_quantity': 0,
            'p1_payoff': c(0),
            'p2_payoff': c(0)
        },
        {
            'p1_quantity': Constants.max_units_per_player,
            'p2_quantity': Constants.max_units_per_player,
            'p1_payoff': c(0),
            'p2_payoff': c(0),
        },
        {
            'p1_quantity': 0,
            'p2_quantity': Constants.max_units_per_player,
            'p1_payoff': c(0),
            'p2_payoff': c(30 * 30),
        }
    ]

    def play_round(self):

        case = self.case
        yield (views.Introduction)

        if self.player.id_in_group == 1:
            yield (views.ChoiceOne, {'quantity': case['p1_quantity']})
            assert self.player.payoff == case['p1_payoff']

        elif self.player.id_in_group == 2:
            yield (views.ChoiceTwo, {'quantity': case['p2_quantity']})
            assert self.player.payoff == case['p2_payoff']

        yield (views.Results)
