# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-ptree-docs/wiki"""

from ptree.db import models
import ptree.models

doc = """
Matrix Asymmetric is a game where there is no identical strategy sets for both players.
Each player earns the different payoff when making the same choice against similar choices of his competitors.

<p>Source code <a href="https://github.com/wickens/ptree_library/tree/master/matrix_asymmetric">here</a></p>
"""


class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'matrix_asymmetric'


class Treatment(ptree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    rowAcolumnA_row = models.MoneyField(default=0.20)
    rowAcolumnA_column = models.MoneyField(default=0.30)

    rowAcolumnB_row = models.MoneyField(default=0.40)
    rowAcolumnB_column = models.MoneyField(default=0.10)

    rowBcolumnA_row = models.MoneyField(default=0.05)
    rowBcolumnA_column = models.MoneyField(default=0.45)

    rowBcolumnB_row = models.MoneyField(default=0.15)
    rowBcolumnB_column = models.MoneyField(default=0.25)


class Match(ptree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    participants_per_match = 2

class Participant(ptree.models.BaseParticipant):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    def other_participant(self):
        """Returns other participant in match"""
        return self.other_participants_in_match()[0]

    decision = models.CharField(
        default=None,
        choices=['A', 'B'],
        doc='either A or B',
    )

    def set_payoff(self):
        if self.role() == 'row':
            payoff_matrix = {
                'A': {
                    'A': self.treatment.rowAcolumnA_row,
                    'B': self.treatment.rowAcolumnB_row,
                },
                'B': {
                    'A': self.treatment.rowBcolumnA_row,
                    'B': self.treatment.rowBcolumnB_row,
                }
            }

        else: #column
            payoff_matrix = {
                'A': {
                    'A': self.treatment.rowAcolumnA_column,
                    'B': self.treatment.rowAcolumnB_column,
                },
                'B': {
                    'A': self.treatment.rowBcolumnA_column,
                    'B': self.treatment.rowBcolumnB_column,
                }
            }

        row_participant = self.match.get_participant_by_role('row')
        column_participant = self.match.get_participant_by_role('column')
        self.payoff = payoff_matrix[row_participant.decision][column_participant.decision]

    def role(self):
        if self.index_among_participants_in_match == 1:
            return 'row'
        if self.index_among_participants_in_match == 2:
            return 'column'


def treatments():
    return [Treatment.create()]