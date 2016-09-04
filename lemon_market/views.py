from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from otree.common import safe_json


class Introduction(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1


class Production(Page):
    def is_displayed(self):
        return self.player.role().startswith('seller')

    form_model = models.Player
    form_fields = ['seller_proposed_price', 'seller_proposed_quality']


class SimpleWaitPage(WaitPage):
    pass


class Purchase(Page):
    def is_displayed(self):
        return self.player.role() == 'buyer'

    form_model = models.Group
    form_fields = ['seller_id']


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoff()


class Results(Page):
    def vars_for_template(self):
        return {'seller': self.group.get_seller()}


class FinalResults(Page):
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):
        # Filling the data for HighCharts graph

        series = []

        transaction_prices = [g.sale_price for g in self.group.in_all_rounds()]
        series.append({
            'name': 'Transaction Price',
            'data': transaction_prices})

        for player in self.group.get_players():
            payoffs = [p.payoff for p in player.in_all_rounds()]
            series.append(
                {'name': 'Earnings for %s' % player.role().capitalize(),
                 'data': payoffs})
        highcharts_series = safe_json(series)

        round_numbers = safe_json(list(range(1, Constants.num_rounds + 1)))

        return {
            'highcharts_series': highcharts_series,
            'round_numbers': round_numbers
        }


page_sequence = [
    Introduction,
    Production,
    SimpleWaitPage,
    Purchase,
    ResultsWaitPage,
    Results,
    FinalResults,
]
