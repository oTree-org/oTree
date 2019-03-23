from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants

class PlayerBot(Bot):

    def play_round(self):
        yield (pages.Introduction)
        if self.player.id_in_group == 1:
            yield (pages.Offer, {'amount_offered': c(10)})
        else:
            if self.group.use_strategy_method:
                yield (pages.AcceptStrategy, {'response_{}'.format(
                    int(offer)): True for offer in Constants.offer_choices})
            else:
                yield (pages.Accept, {'offer_accepted': True})
        yield (pages.Results)



