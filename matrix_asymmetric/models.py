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
    subsession = models.ForeignKey(Subsession)

    rowAcolumnA_row = models.PositiveIntegerField()
    rowAcolumnA_column = models.PositiveIntegerField()

    rowAcolumnB_row = models.PositiveIntegerField()
    rowAcolumnB_column = models.PositiveIntegerField()

    rowBcolumnA_row = models.PositiveIntegerField()
    rowBcolumnA_column = models.PositiveIntegerField()

    rowBcolumnB_row = models.PositiveIntegerField()
    rowBcolumnB_column = models.PositiveIntegerField()


class Match(ptree.models.BaseMatch):

    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)

    participants_per_match = 2

    def row_participant(self):
        for p in self.participants():
            if p.role() == 'row':
                return p

    def column_participant(self):
        for p in self.participants():
            if p.role() == 'column':
                return p


class Participant(ptree.models.BaseParticipant):

    match = models.ForeignKey(Match, null = True)
    treatment = models.ForeignKey(Treatment, null = True)
    subsession = models.ForeignKey(Subsession)

    def other_participant(self):
        """Returns other participant in match"""
        return self.other_participants_in_match()[0]

    decision = models.CharField(
        null=True,
        max_length=2,
        choices=(('A', 'A'), ('B', 'B')),
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
        self.payoff = payoff_matrix[self.match.row_participant().decision][self.match.column_participant().decision]

    def role(self):
        return {
            1: 'row',
            2: 'column'
        }[self.index_among_participants_in_match]


def treatments():

    treatment_list = []

    treatment = Treatment(

        rowAcolumnA_row=20,
        rowAcolumnA_column=30,

        rowAcolumnB_row=40,
        rowAcolumnB_column=10,

        rowBcolumnA_row=5,
        rowBcolumnA_column=45,

        rowBcolumnB_row=15,
        rowBcolumnB_column=25,
    )

    treatment_list.append(treatment)

    return treatment_list