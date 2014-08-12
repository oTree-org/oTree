# -*- coding: utf-8 -*-
import otree.views
import otree.views.concrete
import tragedy_of_the_commons.forms as forms
from tragedy_of_the_commons.utilities import Page, MatchWaitPage, SubsessionWaitPage
from otree.common import Money, money_range


class Introduction(Page):

    def participate_condition(self):
        return True

    template_name = 'tragedy_of_the_commons/Introduction.html'

    def variables_for_template(self):

        return {
            'common_gain': self.treatment.common_gain,
            'common_loss': self.treatment.common_loss,
            'common_cost': self.treatment.individual_gain - self.treatment.defect_costs,
            'defect_gain': self.treatment.common_gain - self.treatment.defect_costs,
        }


class Decision(Page):

    def participate_condition(self):
        return True

    template_name = 'tragedy_of_the_commons/Decision.html'

    def get_form_class(self):
        return forms.DecisionForm


class ResultsWaitPage(MatchWaitPage):

    def action(self):
        for p in self.match.players():
            p.set_payoff()


class Results(Page):

    template_name = 'tragedy_of_the_commons/Results.html'

    def variables_for_template(self):
        return {
            'payoff': self.player.payoff,
        }


def pages():
    return [
        Introduction,
        Decision,
        ResultsWaitPage,
        Results
    ]