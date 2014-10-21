# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
from otree import widgets
from otree.common import Money
# </standard imports>


doc = """
In a lemon market of Akerlof (1970), 2 buyers and 1 seller interact for 3
periods. The implementation is based on Holt (1999).

Source code <a
href='https://github.com/oTree-org/oTree/tree/master/lemon_market'>here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'lemon_market'


class Group(otree.models.BaseGroup):
    INITIAL = 100

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    buyer_choice = models.PositiveIntegerField()
    players_per_group = 3

    def set_payoff(self):
        for p in self.get_players():
            p.payoff = self.INITIAL
        buyer = self.get_player_by_id(1)
        if buyer.choice:
            seller = self.get_player_by_id(buyer.choice + 1)
            buyer.payoff += seller.quality + 5 - seller.price
            seller.payoff += seller.price - seller.quality

    def seller(self):
        choice = self.get_player_by_role('buyer')
        if choice:
            return self.get_player_by_id(choice + 1)


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>
    # training
    training_buyer_earnings = models.IntegerField(
        verbose_name="Buyer's earning would be")
    training_seller1_earnings = models.IntegerField(
        verbose_name="Seller 1's earning would be")
    training_seller2_earnings = models.IntegerField(
        verbose_name="Seller 2's earning would be")
    # seller
    price = models.PositiveIntegerField(
        verbose_name='Please indicate a price you want to sell')
    quality = models.PositiveIntegerField(choices=[
        (30, 'High'),
        (20, 'Medium'),
        (10, 'Low')],
        verbose_name='Please select a quality grade you want to produce',
        widget=widgets.RadioSelectHorizontal())
    # buyer
    choice = models.PositiveIntegerField(
        blank=True, widget=widgets.RadioSelect())  # seller index
    feedback = models.PositiveIntegerField(
        choices=(
            (5, 'Very well'),
            (4, 'Well'),
            (3, 'OK'),
            (2, 'Badly'),
            (1, 'Very badly')), widget=widgets.RadioSelectHorizontal(),
        verbose_name='')

    def choice_choices(self):
        return [(i, 'Buy from seller %i' % i) for i in range(
            1, self.group.players_per_group)] + [(0, 'Buy nothing')]

    def role(self):
        if self.id_in_group == 1:
            return 'buyer'
        return 'seller %i' % (self.id_in_group - 1)

    def earnings(self):
        return self.payoff - self.group.INITIAL
