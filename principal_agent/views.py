# -*- coding: utf-8 -*-
import ptree.views
import ptree.views.concrete
import principal_agent.forms as forms
from principal_agent.utilities import ParticipantMixIn, MatchMixIn
from ptree.common import currency


class Introduction(ParticipantMixIn, ptree.views.Page):

    def show_skip_wait(self):
        return self.PageActions.show

    template_name = 'principal_agent/Introduction.html'

    def variables_for_template(self):
        return {
            'fixed_payment': self.treatment.fixed_payment,
            'reject_prncpl_pay': currency(0),
            'reject_agt_pay': currency(100)
        }


class Offer(ParticipantMixIn, ptree.views.Page):

    def participate_condition(self):
        return self.participant.index_among_participants_in_match == 1

    template_name = 'principal_agent/Offer.html'

    def get_form_class(self):
        return forms.ContractForm

    def variables_for_template(self):
        return {
            'fixed_payment': self.treatment.fixed_payment,
        }


class SimpleCheckpoint(MatchMixIn, ptree.views.MatchCheckpoint):

    def wait_page_body_text(self):
        return 'Please wait for the other participant.'


class Accept(ParticipantMixIn, ptree.views.Page):

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


class WorkEffort(ParticipantMixIn, ptree.views.Page):

    template_name = 'principal_agent/WorkEffort.html'

    def get_form_class(self):
        return forms.WorkEffortForm

    def participate_condition(self):
        if self.match.decision == 'Accept':
            return self.participant.index_among_participants_in_match == 2


class ResultsCheckpoint(MatchMixIn, ptree.views.MatchCheckpoint):

    def action(self):
        for p in self.match.participants():
            p.set_payoff()

    def wait_page_body_text(self):
        return "Waiting for the other participant."


class Results(ParticipantMixIn, ptree.views.Page):

    template_name = 'principal_agent/Results.html'

    def variables_for_template(self):
        if self.participant.payoff is None:
            self.participant.set_payoff()
        return {
            'payoff': currency(self.participant.payoff),
            'rejected': True if self.match.decision == 'Reject' else False,
            'agent': True if self.participant.index_among_participants_in_match == 2 else False
        }


def pages():
    return [
        Introduction,
        Offer,
        SimpleCheckpoint,
        Accept,
        WorkEffort,
        ResultsCheckpoint,
        Results
    ]