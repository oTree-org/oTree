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
This is a one-period public goods game with 3 players. Assignment to groups is
random.

"""


source_code = "https://github.com/oTree-org/oTree/tree/master/public_goods"


bibliography = ()


links = {
    "Wikipedia": {
        "Public Goods Game": "https://en.wikipedia.org/wiki/Public_goods_game"
    }
}


keywords = ("Public Goods",)


class Constants(BaseConstants):
    name_in_url = 'public_goods'
    players_per_group = 3
    num_rounds = 1

    #"""Amount allocated to each player"""
    endowment = c(100)
    efficiency_factor = 1.8
    base_points = c(10)

    question_correct = c(92)


class Subsession(BaseSubsession):

    pass


class Group(BaseGroup):

    total_contribution = models.CurrencyField()

    individual_share = models.CurrencyField()

    def set_payoffs(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.individual_share = self.total_contribution * Constants.efficiency_factor / Constants.players_per_group
        for p in self.get_players():
            p.payoff = (Constants.endowment - p.contribution) + self.individual_share + Constants.base_points


class Player(BasePlayer):

    contribution = models.CurrencyField(
        min=0, max=Constants.endowment,
        doc="""The amount contributed by the player""",
    )

    question = models.CurrencyField()

    def question_correct(self):
        return self.question == Constants.question_correct



