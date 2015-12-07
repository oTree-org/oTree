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
This is a standard 2-player trust game where the amount sent by player 1 gets
tripled. The trust game was first proposed by
<a href="http://econweb.ucsd.edu/~jandreon/Econ264/papers/Berg%20et%20al%20GEB%201995.pdf" target="_blank">
    Berg, Dickhaut, and McCabe (1995)
</a>.
"""


source_code = "https://github.com/oTree-org/oTree/tree/master/trust"


bibliography = ()


links = {}


keywords = ("Trust Game",)


class Constants(BaseConstants):
    name_in_url = 'trust'
    players_per_group = 2
    num_rounds = 1

    #Initial amount allocated to each player
    amount_allocated = c(100)
    multiplication_factor = 3
    bonus = c(10)

    training_answer_x_correct = c(130)
    training_answer_y_correct = c(10)

class Subsession(BaseSubsession):

    pass



class Group(BaseGroup):


    sent_amount = models.CurrencyField(
        min=0, max=Constants.amount_allocated,
        doc="""Amount sent by P1""",
    )

    sent_back_amount = models.CurrencyField(
        doc="""Amount sent back by P2""",
        min=c(0),
    )

    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p1.payoff = Constants.bonus + Constants.amount_allocated - self.sent_amount + self.sent_back_amount
        p2.payoff = Constants.bonus + self.sent_amount * Constants.multiplication_factor - self.sent_back_amount


class Player(BasePlayer):

    training_answer_x = models.CurrencyField(verbose_name='Participant A would have')
    training_answer_y = models.CurrencyField(verbose_name='Participant B would have')

    def role(self):
        return {1: 'A', 2: 'B'}[self.id_in_group]
