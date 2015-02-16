# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants

class Decision(Page):

    form_model = models.Player
    form_fields = ['decision']

    # def vars_for_template(self):
    #     return {'player_id': self.player.id_in_group,
    #             'rowAcolumnA_row': Constants.rowAcolumnA_row,
    #             'rowAcolumnA_column': Constants.rowAcolumnA_column,
    #             'rowAcolumnB_row': Constants.rowAcolumnB_row,
    #             'rowAcolumnB_column': Constants.rowAcolumnB_column,
    #             'rowBcolumnA_row': Constants.rowBcolumnA_row,
    #             'rowBcolumnA_column': Constants.rowBcolumnA_column,
    #             'rowBcolumnB_row': Constants.rowBcolumnB_row,
    #             'rowBcolumnB_column': Constants.rowBcolumnB_column}


class ResultsWaitPage(WaitPage):



    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):


    def vars_for_template(self):
        return {
            'same_choice': self.player.decision == self.player.other_player().decision
        }


page_sequence = [Decision,
            ResultsWaitPage,
            Results]
