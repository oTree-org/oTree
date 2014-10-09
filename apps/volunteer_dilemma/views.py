# -*- coding: utf-8 -*-
from __future__ import division
import volunteer_dilemma.models as models
from volunteer_dilemma._builtin import Page, WaitPage


class Decision(Page):

    template_name = 'volunteer_dilemma/Decision.html'

    form_model = models.Player
    form_fields = ['volunteer']

    def variables_for_template(self):
        return {'general_benefit': self.subsession.general_benefit,
                'volunteer_cost': self.subsession.volunteer_cost,
                'num_other_players': self.group.players_per_group - 1}


class ResultsWaitPage(WaitPage):

    scope = models.Group

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):

    template_name = 'volunteer_dilemma/Results.html'

    def variables_for_template(self):
        return {'volunteer': self.player.volunteer,
                'payoff': self.player.payoff,
                'num_volunteers': len([p for p in self.group.players if p.volunteer])}


def pages():

    return [Decision,
            ResultsWaitPage,
            Results]
