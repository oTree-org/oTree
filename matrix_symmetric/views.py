# -*- coding: utf-8 -*-
import matrix_symmetric.forms as forms
from matrix_symmetric.utilities import Page, MatchWaitPage, SubsessionWaitPage
from otree.common import Money, money_range


class Decision(Page):

    template_name = 'matrix_symmetric/Decision.html'

    def get_form_class(self):
        return forms.DecisionForm

    def variables_for_template(self):
        return {
            'self_A_other_A': self.treatment.self_A_other_A,
            'self_A_other_B': self.treatment.self_A_other_B,
            'self_B_other_A': self.treatment.self_B_other_A,
            'self_B_other_B': self.treatment.self_B_other_B,
        }


class ResultsWaitPage(MatchWaitPage):

    def action(self):
        for p in self.match.players():
            p.set_payoff()

    def body_text(self):
        return "Waiting for the other player."


class Results(Page):

    template_name = 'matrix_symmetric/Results.html'

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