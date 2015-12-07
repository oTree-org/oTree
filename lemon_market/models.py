# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer

from otree import widgets
from otree.common import Currency as c, currency_range
# </standard imports>


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

source_code = "https://github.com/oTree-org/oTree/tree/master/lemon_market"


bibliography = ()


links = {
    "Wikipedia": {
        "The Market for Lemons":
            "https://en.wikipedia.org/wiki/The_Market_for_Lemons"
    }
}


keywords = ("Lemon Market",)





class Constants(BaseConstants):
    name_in_url = 'lemon_market'
    players_per_group = 3
    num_rounds = 3
    participation_fee = c(10)
    INITIAL = c(50)


class Subsession(BaseSubsession):

    final = models.BooleanField(initial=False)


class Group(BaseGroup):

    buyer_choice = models.PositiveIntegerField()

    def set_payoff(self):
        for p in self.get_players():
            p.payoff = Constants.INITIAL
        buyer = self.get_player_by_id(1)

        if buyer.choice:
            seller = self.get_player_by_id(buyer.choice + 1)
            buyer.payoff += seller.quality + 5 - seller.price
            seller.payoff += seller.price - seller.quality

    def seller(self):
        choice = self.get_player_by_role('buyer').choice
        if choice:
            return self.get_player_by_id(choice + 1)


class Player(BasePlayer):

    # training
    training_buyer_earnings = models.CurrencyField(
        verbose_name="Buyer's period payoff would be")

    training_seller1_earnings = models.CurrencyField(
        verbose_name="Seller 1's period payoff would be")

    training_seller2_earnings = models.CurrencyField(
        verbose_name="Seller 2's period payoff would be")

    # seller
    price = models.CurrencyField(
        min=0, max=Constants.INITIAL,
        verbose_name='Please indicate a price (from 0 to %i) you want to sell'
        % Constants.INITIAL)

    quality = models.CurrencyField(choices=[
        (30, 'High'),
        (20, 'Medium'),
        (10, 'Low')],
        verbose_name='Please select a quality grade you want to produce',
        widget=widgets.RadioSelectHorizontal())

    # buyer
    choice = models.PositiveIntegerField(
        choices=[(i, 'Buy from seller %i' % i) for i in
                 range(1, Constants.players_per_group)] + [(0, 'Buy nothing')],
        blank=True,
        widget=widgets.RadioSelect(),
        verbose_name='And you will')  # seller index

    def role(self):
        if self.id_in_group == 1:
            return 'buyer'
        return 'seller %i' % (self.id_in_group - 1)
