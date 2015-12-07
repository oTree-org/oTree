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
In the asymmetric matrix game, the strategy sets for both players are
different.
"""

source_code = "https://github.com/oTree-org/oTree/tree/master/matrix_asymmetric"


bibliography = ()


links = {}


keywords = ()


class Constants(BaseConstants):
    name_in_url = 'matrix_asymmetric'
    players_per_group = 2
    num_rounds = 1

    rowAcolumnA_row = c(20)
    rowAcolumnA_column = c(30)

    # Amount row player gets, if row player chooses A and column player chooses B
    rowAcolumnB_row = c(40)
    rowAcolumnB_column = c(10)

    rowBcolumnA_row = c(5)
    rowBcolumnA_column = c(45)

    rowBcolumnB_row = c(15)
    rowBcolumnB_column = c(25)


class Subsession(BaseSubsession):

    pass



class Group(BaseGroup):

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


class Player(BasePlayer):

    def other_player(self):
        """Returns other player in group"""
        return self.get_others_in_group()[0]

    decision = models.CharField(
        choices=['A', 'B'],
        doc='either A or B',
        widget=widgets.RadioSelect()
    )

    def role(self):
        if self.id_in_group == 1:
            return 'column'
        if self.id_in_group == 2:
            return 'row'


