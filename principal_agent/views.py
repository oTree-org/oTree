# -*- coding: utf-8 -*-
import principal_agent.forms as forms
from principal_agent.utilities import Page, MatchWaitPage, SubsessionWaitPage
from ptree.common import currency


class Introduction(Page):

    template_name = 'principal_agent/Introduction.html'

    def variables_for_template(self):
        return {
            'fixed_payment': self.treatment.fixed_payment,
            'reject_prncpl_pay': currency(0),
            'reject_agt_pay': currency(100)
        }


class Offer(Page):

    def participate_condition(self):
        return self.participant.index_among_participants_in_match == 1

    template_name = 'principal_agent/Offer.html'

    def get_form_class(self):
        return forms.ContractForm

    def variables_for_template(self):
        return {
            'fixed_payment': self.treatment.fixed_payment,
        }


class Accept(Page):

    template_name = 'principal_agent/Accept.html'

    def participate_condition(self):
        return self.participant.index_among_participants_in_match == 2

    def get_form_class(self):
        return forms.DecisionForm

    def variables_for_template(self):
        return {
            'fixed_pay': currency(self.match.agent_fixed_pay),
            'return_share': self.match.agent_return_share,
        }


class WorkEffort(Page):

    template_name = 'principal_agent/WorkEffort.html'

    def get_form_class(self):
        return forms.WorkEffortForm

    def participate_condition(self):
        if self.match.decision == 'Accept':
            return self.participant.index_among_participants_in_match == 2


class ResultsWaitPage(MatchWaitPage):

    def action(self):
        for p in self.match.participants():
            p.set_payoff()

    def body_text(self):
        return "Waiting for the other participant."


class Results(Page):

    template_name = 'principal_agent/Results.html'

    def variables_for_template(self):
        return {
            'payoff': currency(self.participant.payoff),
            'rejected': self.match.decision == 'Reject',
            'agent': self.participant.index_among_participants_in_match == 2
        }


def pages():
    return [
        Introduction,
        Offer,
        MatchWaitPage,
        Accept,
        WorkEffort,
        ResultsWaitPage,
        Results
    ]