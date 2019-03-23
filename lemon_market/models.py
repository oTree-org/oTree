from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


doc = """
In a lemon market of
<a href="http://people.bu.edu/ellisrp/EC387/Papers/1970Akerlof_Lemons_QJE.pdf" target="_blank">
    Akerlof (1970)
</a>, 2 buyers and 1 seller interact for 3 periods. The implementation is
based on
<a href="http://people.virginia.edu/~cah2k/lemontr.pdf" target="_blank">
    Holt (1999)
</a>.
"""


class Constants(BaseConstants):
    name_in_url = 'lemon_market'
    players_per_group = 3
    num_rounds = 3

    instructions_template = 'lemon_market/instructions.html'

    initial_endowment = c(50)
    buyer_extra_value = c(5)

    buy_choices = []
    for i in range(1, players_per_group):
        choice = [i, 'Buy from seller {}'.format(i)]
        buy_choices.append(choice)
    buy_choices.append([0, 'Buy nothing'])

    quality_production_costs = {
        # Level: ProductionCost
        'High': 30,
        'Medium': 20,
        'Low': 10
    }

    quality_level_names = list(quality_production_costs.keys())


class Subsession(BaseSubsession):

    def vars_for_admin_report(self):
        group = self.get_groups()[0]

        series = []

        transaction_prices = [g.sale_price for g in group.in_all_rounds()]
        series.append({
            'name': 'Transaction Price',
            'data': transaction_prices})

        for player in group.get_players():
            payoffs = [p.payoff for p in player.in_all_rounds()]
            series.append(
                {'name': 'Earnings for {}'.format(player.role()),
                 'data': payoffs})

        return {
            'highcharts_series': series,
            'round_numbers': list(range(1, Constants.num_rounds + 1))
        }



class Group(BaseGroup):
    sale_price = models.CurrencyField()
    sale_quality = models.StringField()

    seller_id = models.IntegerField(
        choices=Constants.buy_choices,
        widget=widgets.RadioSelect,
        doc="""0 means no purchase made"""
    )

    def set_payoff(self):
        for p in self.get_players():
            p.payoff = Constants.initial_endowment

        if self.seller_id != 0:
            seller = self.get_player_by_id(self.seller_id)
            buyer = self.get_player_by_role('buyer')

            self.sale_price = seller.seller_proposed_price
            self.sale_quality = seller.seller_proposed_quality
            quality_production_cost = Constants.quality_production_costs[self.sale_quality]
            buyer.payoff += quality_production_cost + Constants.buyer_extra_value - self.sale_price
            seller.payoff += self.sale_price - quality_production_cost


class Player(BasePlayer):
    seller_proposed_price = models.CurrencyField(
        min=0, max=Constants.initial_endowment
    )

    seller_proposed_quality = models.StringField(
        choices=Constants.quality_level_names,
        widget=widgets.RadioSelectHorizontal
    )

    def role(self):
        if self.id_in_group == Constants.players_per_group:
            return 'buyer'
        return 'seller {}'.format(self.id_in_group)
