# -*- coding: utf-8 -*-
import volunteer_dilemma.forms as forms
from volunteer_dilemma._builtin import Page, MatchWaitPage


class Decision(Page):

    template_name = 'volunteer_dilemma/Decision.html'

    def get_form_class(self):
        return forms.DecisionForm

    def variables_for_template(self):
        return {'general_benefit': self.treatment.general_benefit,
                'volunteer_cost': self.treatment.volunteer_cost,
                'num_other_players': self.match.players_per_match - 1}


class ResultsWaitPage(MatchWaitPage):

    def after_all_players_arrive(self):
        self.match.set_payoffs()


class Results(Page):

    template_name = 'volunteer_dilemma/Results.html'

    def variables_for_template(self):
        return {'decision': self.player.decision,
                'payoff': self.player.payoff,
                'num_volunteers': len([p for p in self.match.players if p.decision == 'Volunteer'])}


def pages():

    return [Decision,
            ResultsWaitPage,
            Results]