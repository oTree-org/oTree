# -*- coding: utf-8 -*-
import matrix_asymmetric.forms as forms
from matrix_asymmetric._builtin import Page, MatchWaitPage, SubsessionWaitPage
from otree.common import Money, money_range


class Decision(Page):

    template_name = 'matrix_asymmetric/Decision.html'

    def get_form_class(self):
        return forms.DecisionForm

    def variables_for_template(self):
        return {
            'rowAcolumnA_row': self.treatment.rowAcolumnA_row,
            'rowAcolumnA_column': self.treatment.rowAcolumnA_column,

            'rowAcolumnB_row': self.treatment.rowAcolumnB_row,
            'rowAcolumnB_column': self.treatment.rowAcolumnB_column,

            'rowBcolumnA_row': self.treatment.rowBcolumnA_row,
            'rowBcolumnA_column': self.treatment.rowBcolumnA_column,

            'rowBcolumnB_row': self.treatment.rowBcolumnB_row,
            'rowBcolumnB_column': self.treatment.rowBcolumnB_column,
        }

class ResultsWaitPage(MatchWaitPage):

    def after_all_players_arrive(self):
        self.match.set_payoffs()


class Results(Page):

    template_name = 'matrix_asymmetric/Results.html'

    def variables_for_template(self):
        return {
            'payoff': self.player.payoff,
            'my_decision': self.player.decision,
            'other_decision': self.player.other_player().decision,
            'same_decision': self.player.decision == self.player.other_player().decision,
        }


def pages():
    return [
        Decision,
        ResultsWaitPage,
        Results
    ]