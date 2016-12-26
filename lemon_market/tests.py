from otree.api import Currency as c, currency_range, SubmissionMustFail
from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    cases = ['purchase', 'no_purchase']

    def play_round(self):

        case = self.case

        if self.subsession.round_number == 1:
            yield (views.Introduction)

        if 'seller' in self.player.role():
            yield (
                views.Production,
                {
                    'seller_proposed_price': Constants.initial_endowment,
                    'seller_proposed_quality': 10
                })
            if case == 'purchase':
                assert 'at a price of <strong>{}'.format(
                    Constants.initial_endowment) in self.html
            else:
                assert 'The buyer bought nothing' in self.html
        else:
            # can't make a null purchase
            yield SubmissionMustFail(views.Purchase)
            if case == 'purchase':
                yield (views.Purchase, {'seller_id': 1})
                assert 'The quality grade of your purchase is <strong>Low' in self.html
                assert 'your period payoff is <strong>{}'.format(
                    c(15)) in self.html
            else:
                yield (views.Purchase, {'seller_id': 0})
                assert 'You bought nothing' in self.html
                assert "your period payoff is {}".format(Constants.initial_endowment)

        yield (views.Results)
        if self.subsession.round_number == Constants.num_rounds:
            yield (views.FinalResults)
