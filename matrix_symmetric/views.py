# -*- coding: utf-8 -*-
from __future__ import division
import matrix_symmetric.models as models
from matrix_symmetric._builtin import Page, WaitPage


class Decision(Page):

    template_name = 'matrix_symmetric/Decision.html'

    form_model = models.Player
    form_fields = ['decision']

    def variables_for_template(self):
        return {'self_A_other_A': self.subsession.self_A_other_A,
                'self_A_other_B': self.subsession.self_A_other_B,
                'self_B_other_A': self.subsession.self_B_other_A,
                'self_B_other_B': self.subsession.self_B_other_B}


class ResultsWaitPage(WaitPage):

    scope = models.Group

    def after_all_players_arrive(self):
        for p in self.group.players:
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
