# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
from otree import widgets
from otree.common import Money, money_range
import random
from utils import FEEDBACK_CHOICES
# </standard imports>


doc = """
2 firms complete in a market by setting prices for homogenous goods.
Source code <a
href="https://github.com/oTree-org/oTree/tree/master/bertrand_competition"
target="_blank">here</a>.
"""
# Recommended Literature
# Kruse, Jamie Brown, et al. "Bertrand-Edgeworth competition in experimental
# markets." Econometrica: Journal of the Econometric Society (1994):
# Dufwenberg, Martin, and Uri Gneezy. "Price competition and market
# concentration: an experimental study." International Journal of Industrial
# Organization 18.1
# http://en.wikipedia.org/wiki/Bertrand_competition


class Constants:
    bonus = 10
    maximum_price = 100


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'bertrand_competition'


class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_group = 2

    def set_payoffs(self):
        players = self.get_players()
        winning_price = min([p.price for p in players])
        winners = [p for p in players if p.price == winning_price]
        winner = random.choice(winners)
        for p in players:
            p.payoff = Constants.bonus
            if p == winner:
                p.is_a_winner = True
                p.payoff += p.price


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>
    training_my_profit = models.PositiveIntegerField(
        verbose_name='My profit would be')

    price = models.PositiveIntegerField(
        doc="""Price player chooses to sell product for"""
    )

    is_a_winner = models.BooleanField(
        default=False,
        doc="""Whether this player offered lowest price"""
    )

    feedback = models.PositiveIntegerField(
        choices=FEEDBACK_CHOICES, widget=widgets.RadioSelectHorizontal(),
        verbose_name='')

    def price_error_message(self, value):
        if not 0 <= value <= Constants.maximum_price:
            return 'Your entry is invalid.'

    def is_sole_winner(self):
        return self.is_a_winner and self.group.num_winners == 1

    def is_shared_winner(self):
        return self.is_a_winner and self.group.num_winners > 1
