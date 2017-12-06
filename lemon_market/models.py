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

    instructions_template = 'lemon_market/Instructions.html'

    initial_endowment = c(50)
    buyer_extra_value = c(5)


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
                {'name': 'Earnings for %s' % player.role().capitalize(),
                 'data': payoffs})

        return {
            'highcharts_series': series,
            'round_numbers': list(range(1, Constants.num_rounds + 1))
        }



class Group(BaseGroup):
    sale_price = models.CurrencyField()

    seller_id = models.IntegerField(
        choices=[(i, 'Buy from seller %i' % i) for i in
                 range(1, Constants.players_per_group)] + [
                    (0, 'Buy nothing')],
        widget=widgets.RadioSelect,
        doc="""0 means no purchase made"""
    )  # seller index

    def set_payoff(self):
        for p in self.get_players():
            p.payoff = Constants.initial_endowment

        if self.seller_id != 0:
            seller = self.get_seller()
            self.sale_price = seller.seller_proposed_price

            buyer = self.get_player_by_role('buyer')
            buyer.payoff += seller.seller_proposed_quality + Constants.buyer_extra_value - seller.seller_proposed_price
            seller.payoff += seller.seller_proposed_price - seller.seller_proposed_quality

    def get_seller(self):
        for p in self.get_players():
            if 'seller' in p.role() and p.seller_id() == self.seller_id:
                return p


class Player(BasePlayer):
    # seller
    seller_proposed_price = models.CurrencyField(
        min=0, max=Constants.initial_endowment
    )

    seller_proposed_quality = models.CurrencyField(
        choices=[
            (30, 'High'),
            (20, 'Medium'),
            (10, 'Low')],
        widget=widgets.RadioSelectHorizontal)

    def seller_id(self):
        # player 1 is the buyer, so seller 1 is actually player 2
        return (self.id_in_group - 1)

    def role(self):
        if self.id_in_group == 1:
            return 'buyer'
        return 'seller {}'.format(self.seller_id())
