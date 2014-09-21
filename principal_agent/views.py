# -*- coding: utf-8 -*-
import principal_agent.forms as forms
from principal_agent._builtin import Page, MatchWaitPage, SubsessionWaitPage
from otree.common import Money, money_range


def variables_for_all_templates(self):

    efforts_returns_costs = []
    for effort in range(1, 10+1):
        efforts_returns_costs.append(
            [effort,
             self.treatment.return_from_effort(effort),
             self.treatment.cost_from_effort(effort)]
        )

    return {'fixed_payment': self.treatment.max_fixed_payment,
            'reject_principal_pay': self.treatment.reject_principal_pay,
            'reject_agent_pay': self.treatment.reject_agent_pay,
            'efforts_returns_costs': efforts_returns_costs}


class Introduction(Page):

    template_name = 'principal_agent/Introduction.html'


class Offer(Page):

    def participate_condition(self):
        return self.player.role() == 'principal'

    template_name = 'principal_agent/Offer.html'

    def get_form_class(self):
        return forms.ContractForm


class Accept(Page):

    template_name = 'principal_agent/Accept.html'

    def participate_condition(self):
        return self.player.role() == 'agent'

    def get_form_class(self):
        return forms.DecisionForm

    def variables_for_template(self):
        return {'fixed_pay': self.match.agent_fixed_pay,
                'return_share': int(self.match.agent_return_share * 100)}


class WorkEffort(Page):

    template_name = 'principal_agent/WorkEffort.html'

    def get_form_class(self):
        return forms.WorkEffortForm

    def participate_condition(self):
        return self.player.role() == 'agent' and self.match.contract_accepted


class ResultsWaitPage(MatchWaitPage):

    def after_all_players_arrive(self):
        self.match.set_payoffs()


class Results(Page):

    template_name = 'principal_agent/Results.html'

    def variables_for_template(self):
        return {'payoff': self.player.payoff,
                'accepted': self.match.contract_accepted,
                'agent': self.player.role() == 'agent'}


def pages():
    return [Introduction,
            Offer,
            MatchWaitPage,
            Accept,
            WorkEffort,
            ResultsWaitPage,
            Results]
