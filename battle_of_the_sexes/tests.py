from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants

class PlayerBot(Bot):
    cases = ['both_football', 'mismatch']

    def play_round(self):
        yield (views.Introduction)

        if self.case == 'both_football':
            yield (views.Decide, {"decision": 'Football'})
            if self.player.role() == 'husband':
                assert self.player.payoff == Constants.football_husband_payoff
            else:
                assert self.player.payoff == Constants.football_wife_payoff

        if self.case == 'mismatch':
            if self.player.role() == 'husband':
                yield (views.Decide, {"decision": 'Football'})
            else:
                yield (views.Decide, {"decision": 'Opera'})
            assert self.player.payoff == Constants.mismatch_payoff

        yield (views.Results)
