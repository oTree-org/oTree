# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Money, money_range
from .models import Constants

class Decision(Page):

    template_name = 'matrix_asymmetric/Decision.html'

    form_model = models.Player
    form_fields = ['decision']

    def variables_for_template(self):
        return {'player_id': self.player.id_in_group,
                'rowAcolumnA_row': self.subsession.rowAcolumnA_row,
                'rowAcolumnA_column': self.subsession.rowAcolumnA_column,
                'rowAcolumnB_row': self.subsession.rowAcolumnB_row,
                'rowAcolumnB_column': self.subsession.rowAcolumnB_column,
                'rowBcolumnA_row': self.subsession.rowBcolumnA_row,
                'rowBcolumnA_column': self.subsession.rowBcolumnA_column,
                'rowBcolumnB_row': self.subsession.rowBcolumnB_row,
                'rowBcolumnB_column': self.subsession.rowBcolumnB_column}


class ResultsWaitPage(WaitPage):

    scope = models.Group

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):

    template_name = 'matrix_asymmetric/Results.html'

    def variables_for_template(self):
        return {'payoff': self.player.payoff,
                'my_choice': self.player.decision,
                'other_choice': self.player.other_player().decision,
                'same_choice': self.player.decision == self.player.other_player().decision}


def pages():

    return [Decision,
            ResultsWaitPage,
            Results]
