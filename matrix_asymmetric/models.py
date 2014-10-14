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
In the asymmetric matrix game, the strategy sets for both players are different.
Source code <a href="https://github.com/oTree-org/oTree/tree/master/matrix_asymmetric" target="_blank">here</a>.
"""

class Constants:
    rowAcolumnA_row = Money(0.20)
    rowAcolumnA_column = Money(0.30)

    # Amount row player gets, if row player chooses A and column player chooses B
    rowAcolumnB_row = Money(0.40)
    rowAcolumnB_column = Money(0.10)

    rowBcolumnA_row = Money(0.05)
    rowBcolumnA_column = Money(0.45)

    rowBcolumnB_row = Money(0.15)
    rowBcolumnB_column = Money(0.25)


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'matrix_asymmetric'



class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_group = 2

    def set_payoffs(self):
        row_player = self.get_player_by_role('row')
        column_player = self.get_player_by_role('column')

        row_matrix = {
            'A': {
                'A': Constants.rowAcolumnA_row,
                'B': Constants.rowAcolumnB_row,
            },
            'B': {
                'A': Constants.rowBcolumnA_row,
                'B': Constants.rowBcolumnB_row,
            }
        }

        column_matrix = {
            'A': {
                'A': Constants.rowAcolumnA_column,
                'B': Constants.rowAcolumnB_column,
            },
            'B': {
                'A': Constants.rowBcolumnA_column,
                'B': Constants.rowBcolumnB_column,
            }
        }

        row_player.payoff = row_matrix[row_player.decision][column_player.decision]
        column_player.payoff = column_matrix[row_player.decision][column_player.decision]


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
        widget=widgets.RadioSelect()
    )

    def decision_choices(self):
        return ['A', 'B']

    def role(self):
        if self.id_in_group == 1:
            return 'column'
        if self.id_in_group == 2:
            return 'row'


