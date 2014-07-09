# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-ptree-docs/wiki"""

from ptree.db import models
import ptree.models

doc = """
Description of this app.

<p>Source code <a href="https://github.com/wickens/ptree_library/tree/master/matrix_asymmetric">here</a></p>
"""

class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'matrix_asymmetric'


class Treatment(ptree.models.BaseTreatment):
    subsession = models.ForeignKey(Subsession)

    r1c1_row = models.PositiveIntegerField()
    r1c1_column = models.PositiveIntegerField()

    r1c2_row = models.PositiveIntegerField()
    r1c2_column = models.PositiveIntegerField()

    r2c1_row = models.PositiveIntegerField()
    r2c1_column = models.PositiveIntegerField()

    r2c2_row = models.PositiveIntegerField()
    r2c2_column = models.PositiveIntegerField()

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


    decision = models.PositiveIntegerField(
        null=True,
        doc='either 1 or 2',
    )

    def set_payoff(self):
        if self.role() == 'row':
            payoff_matrix = {
                1: {
                    1: self.treatment.r1c1_row,
                    2: self.treatment.r1c2_row,
                },
                2: {
                    1: self.treatment.r2c1_row,
                    2: self.treatment.r2c2_row,
                }
            }

        else: #column
            payoff_matrix = {
                1: {
                    1: self.treatment.r1c1_column,
                    2: self.treatment.r1c2_column,
                },
                2: {
                    1: self.treatment.r2c1_column,
                    2: self.treatment.r2c2_column,
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
        label = '',
        # other attributes here...
    )

    treatment_list.append(treatment)

    return treatment_list