# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Money, money_range
from .models import Constants

class Decision(Page):

    template_name = 'matrix_symmetric/Decision.html'

    form_model = models.Player
    form_fields = ['decision']

    def variables_for_template(self):
        return {'self_A_other_A': Constants.self_A_other_A,
                'self_A_other_B': Constants.self_A_other_B,
                'self_B_other_A': Constants.self_B_other_A,
                'self_B_other_B': Constants.self_B_other_B}


class ResultsWaitPage(WaitPage):

    scope = models.Group

    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_payoff()

    def body_text(self):
        return "Waiting for the other player."


class Results(Page):

    template_name = 'matrix_symmetric/Results.html'

    def variables_for_template(self):

        return {'payoff': self.player.payoff,
                'my_choice': self.player.decision,
                'other_choice': self.player.other_player().decision,
                'same_choice': self.player.decision == self.player.other_player().decision}


def pages():

    return [Decision,
            ResultsWaitPage,
            Results]
