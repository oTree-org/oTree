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
In the symmetric matrix game, the payoffs for playing a particular strategy
depend only on the other strategies employed, not on who is playing them.
"""

source_code = "https://github.com/oTree-org/oTree/tree/master/matrix_symmetric"


bibliography = ()


links = {}


keywords = ()


class Constants(BaseConstants):
    name_in_url = 'matrix_symmetric'
    players_per_group = 2
    num_rounds = 1

    self_A_other_A = c(10)

    # How much I make if I choose A and the other player chooses B
    self_A_other_B = c(0)

    self_B_other_A = c(30)
    self_B_other_B = c(40)


class Subsession(BaseSubsession):

    pass



class Group(BaseGroup):


class Player(BasePlayer):

    def other_player(self):
        """Returns other player in group"""
        return self.get_others_in_group()[0]

    decision = models.CharField(
        choices=['A', 'B'],
        doc='either A or B',
        widget=widgets.RadioSelect(),
    )

    def set_payoff(self):

        payoff_matrix = {
            'A': {
                'A': Constants.self_A_other_A,
                'B': Constants.self_A_other_B,
            },
            'B': {
                'A': Constants.self_B_other_A,
                'B': Constants.self_B_other_B,
            }
        }

        self.payoff = payoff_matrix[self.decision][self.other_player().decision]


