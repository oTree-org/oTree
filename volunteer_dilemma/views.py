# -*- coding: utf-8 -*-
import volunteer_dilemma.forms as forms
from volunteer_dilemma.utilities import Page, MatchWaitPage, SubsessionWaitPage
from otree.common import Money, money_range


class Decision(Page):

    template_name = 'volunteer_dilemma/Decision.html'

    def get_form_class(self):
        return forms.DecisionForm

    def variables_for_template(self):
        vol_ign = self.treatment.general_benefit - self.treatment.volunteer_cost
        vol_vol = self.treatment.general_benefit - self.treatment.volunteer_cost
        ign_vol = self.treatment.general_benefit
        ign_ign = 0

        return {
            'vol_ign': vol_ign,
            'ign_vol': ign_vol,
            'vol_vol': vol_vol,
            'ign_ign': ign_ign,
        }

class ResultsWaitPage(MatchWaitPage):

    def action(self):
        for p in self.match.players():
            p.set_payoff()

class Results(Page):

    template_name = 'volunteer_dilemma/Results.html'

    def variables_for_template(self):
        return {
            'decision': self.player.decision,
            'payoff': self.player.payoff,
        }



def pages():
    return [
        Decision,
        ResultsWaitPage,
        Results
    ]