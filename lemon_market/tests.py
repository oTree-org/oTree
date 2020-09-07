from otree.api import Currency as c, currency_range, SubmissionMustFail
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    cases = ['purchase', 'no_purchase']

    def play_round(self):

        case = self.case

        if self.round_number == 1:
            yield (pages.Introduction)

        if 'seller' in self.player.role():
            yield (
                pages.Production,
                {
                    'seller_proposed_price': Constants.initial_endowment,
                    'seller_proposed_quality': 'Low'
                }
            )
            if case == 'purchase':
                msg = 'at a price of {}'.format(Constants.initial_endowment)
                assert msg in self.html
            else:
                assert 'The buyer bought nothing' in self.html
        else:
            # can't make a null purchase
            yield SubmissionMustFail(pages.Purchase)
            if case == 'purchase':
                yield (pages.Purchase, {'seller_id': 1})
                assert 'The quality grade of your purchase is Low' in self.html
                msg = 'your period payoff is <strong>{}</strong>'.format(c(15))
                assert msg in self.html
            else:
                yield (pages.Purchase, {'seller_id': 0})
                assert 'You bought nothing' in self.html
                assert "your period payoff is {}".format(Constants.initial_endowment)

        yield (pages.Results)
        if self.round_number == Constants.num_rounds:
            yield (pages.FinalResults)
