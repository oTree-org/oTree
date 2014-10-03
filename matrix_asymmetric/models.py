# -*- coding: utf-8 -*-
"""Documentation at https://github.com/oTree-org/otree/wiki"""

from otree.db import models
import otree.models
from otree import forms

doc = """
In the asymmetric matrix game, the strategy sets for both players are different.
Source code <a href="https://github.com/oTree-org/oTree/tree/master/matrix_asymmetric" target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'matrix_asymmetric'


class Treatment(otree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    rowAcolumnA_row = models.MoneyField(default=0.20)
    rowAcolumnA_column = models.MoneyField(default=0.30)

    rowAcolumnB_row = models.MoneyField(
        default=0.40,
        doc='''Amount row player gets, if row player chooses A and column player chooses B'''
    )
    rowAcolumnB_column = models.MoneyField(default=0.10)

    rowBcolumnA_row = models.MoneyField(default=0.05)
    rowBcolumnA_column = models.MoneyField(default=0.45)

    rowBcolumnB_row = models.MoneyField(default=0.15)
    rowBcolumnB_column = models.MoneyField(default=0.25)


class Match(otree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_match = 2

    def set_payoffs(self):
        row_player = self.get_player_by_role('row')
        column_player = self.get_player_by_role('column')

        row_matrix = {
            'A': {
                'A': self.treatment.rowAcolumnA_row,
                'B': self.treatment.rowAcolumnB_row,
            },
            'B': {
                'A': self.treatment.rowBcolumnA_row,
                'B': self.treatment.rowBcolumnB_row,
            }
        }

        column_matrix = {
            'A': {
                'A': self.treatment.rowAcolumnA_column,
                'B': self.treatment.rowAcolumnB_column,
            },
            'B': {
                'A': self.treatment.rowBcolumnA_column,
                'B': self.treatment.rowBcolumnB_column,
            }
        }

        row_player.payoff = row_matrix[row_player.decision][column_player.decision]
        column_player.payoff = column_matrix[row_player.decision][column_player.decision]


class Player(otree.models.BasePlayer):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    def other_player(self):
        """Returns other player in match"""
        return self.other_players_in_match()[0]

    decision = models.CharField(
        default=None,
        doc='either A or B',
        widget=forms.RadioSelect()
    )

    def decision_choices(self):
        return ['A', 'B']

    def role(self):
        if self.index_among_players_in_match == 1:
            return 'column'
        if self.index_among_players_in_match == 2:
            return 'row'


def treatments():

    return [Treatment.create()]
