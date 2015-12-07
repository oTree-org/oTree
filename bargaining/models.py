# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random

from otree.db import models
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer

from otree import widgets
from otree.common import Currency as c, currency_range
# </standard imports>

doc = """
This bargaining game involves 2 players. Each demands for a portion of some
available amount. If the sum of demands is no larger than the available
amount, both players get demanded portions. Otherwise, both get nothing.
"""

source_code ="https://github.com/oTree-org/oTree/tree/master/bargaining"


class Constants(BaseConstants):
    name_in_url = 'bargaining'
    players_per_group = 2
    num_rounds = 1

    amount_shared = c(100)
    bonus = c(10)


class Subsession(BaseSubsession):

    pass



class Group(BaseGroup):




    def set_payoffs(self):
        players = self.get_players()
        total_requested_amount = sum([p.request_amount for p in players])
        if total_requested_amount <= Constants.amount_shared:
            for p in players:
                p.payoff = p.request_amount + Constants.bonus
        else:
            for p in players:
                p.payoff = Constants.bonus


class Player(BasePlayer):

    request_amount = models.CurrencyField(
        doc="""
        Amount requested by this player.
        """,
        min=0, max=Constants.amount_shared
    )
    training_amount_mine = models.CurrencyField(
        verbose_name='You would get')
    training_amount_other = models.CurrencyField(
        verbose_name='The other participant would get')

    def other_player(self):
        """Returns the opponent of the current player"""
        return self.get_others_in_group()[0]
