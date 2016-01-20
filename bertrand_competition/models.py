# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer

from otree import widgets
from otree.common import Currency as c, currency_range
import random
# </standard imports>


doc = """
2 firms complete in a market by setting prices for homogenous goods.
"""

source_code = "https://github.com/oTree-org/oTree/tree/master/bertrand_competition"

bibliography = (
    (
        'Kruse, J. B., Rassenti, S., Reynolds, S. S., & Smith, V. L. (1994). '
        'Bertrand-Edgeworth competition in experimental markets. '
        'Econometrica: Journal of the Econometric Society, 343-371.'
    ),
    (
        'Dufwenberg, M., & Gneezy, U. (2000). Price competition and market '
        'concentration: an experimental study. International Journal of '
        'Industrial Organization, 18(1), 7-22.'
    )
)

links = {
    "Wikipedia": {
        "Bertrand Competition":
            "http://en.wikipedia.org/wiki/Bertrand_competition"
    }
}

keywords = ("Bertrand Competition",)


class Constants(BaseConstants):
    players_per_group = 2
    name_in_url = 'bertrand_competition'
    num_rounds = 1
    bonus = c(10)
    maximum_price = c(100)


class Subsession(BaseSubsession):

    pass


class Group(BaseGroup):


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


class Player(BasePlayer):

    training_my_profit = models.CurrencyField(
        verbose_name='My profit would be')

    price = models.CurrencyField(
        min=0, max=Constants.maximum_price,
        doc="""Price player chooses to sell product for"""
    )

    is_a_winner = models.BooleanField(
        initial=False,
        doc="""Whether this player offered lowest price"""
    )

