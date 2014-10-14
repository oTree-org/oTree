# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
from otree import widgets
from otree.common import Money, money_range
import random
# </standard imports>


doc = """
In the symmetric matrix game, the payoffs for playing a particular strategy depend only on the other strategies employed, not on who is playing them.
Source code <a href="https://github.com/oTree-org/oTree/tree/master/matrix_symmetric" target="_blank">here</a>.
"""

class Constants:
    self_A_other_A = Money(0.10)

    # How much I make if I choose A and the other player chooses B
    self_A_other_B = Money(0.00)

    self_B_other_A = Money(0.30)
    self_B_other_B = Money(0.40)


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'matrix_symmetric'



class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_group = 2


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    def other_player(self):
        """Returns other player in group"""
        return self.get_others_in_group()[0]

    decision = models.CharField(
        doc='either A or B',
        widget=widgets.RadioSelect(),
    )

    def decision_choices(self):
        return ['A', 'B']

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


