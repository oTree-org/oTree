# -*- coding: utf-8 -*-
import ptree.views
import ptree.views.concrete
import principal_agent.forms as forms
from principal_agent.utilities import ParticipantMixIn, ExperimenterMixIn
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

    def show_skip_wait(self):
        if self.participant.index_among_participants_in_match == 1:
            return self.PageActions.show
        else:
            return self.PageActions.skip

    template_name = 'principal_agent/Offer.html'

    def get_form_class(self):
        return forms.ContractForm

    def variables_for_template(self):
        return {
            'fixed_payment': self.treatment.fixed_payment,
        }


class Accept(ParticipantMixIn, ptree.views.Page):

    def show_skip_wait(self):
        if self.participant.index_among_participants_in_match == 2:
            if self.match.agent_fixed_pay is None:
                return self.PageActions.wait
            else:
                return self.PageActions.show
        else:
            return self.PageActions.skip

    template_name = 'principal_agent/Accept.html'

    def get_form_class(self):
        return forms.DecisionForm

    def variables_for_template(self):
        return {
            'fixed_pay': currency(self.match.agent_fixed_pay),
            'return_share': self.match.agent_return_share,
        }


class WorkEffort(ParticipantMixIn, ptree.views.Page):

    def show_skip_wait(self):
        if self.participant.index_among_participants_in_match == 2:
            if self.match.decision == 'Accept':
                return self.PageActions.show
            else:
                return self.PageActions.skip
        else:
            return self.PageActions.skip

    template_name = 'principal_agent/WorkEffort.html'

    def get_form_class(self):
        return forms.WorkEffortForm


class Results(ParticipantMixIn, ptree.views.Page):

    def show_skip_wait(self):
        if self.match.decision is not None:
            if self.match.decision == 'Accept':
                if self.match.agent_work_effort is not None:
                    return self.PageActions.show
                else:
                    return self.PageActions.wait
            else:
                return self.PageActions.show
        else:
            return self.PageActions.wait

    template_name = 'principal_agent/Results.html'

    def variables_for_template(self):
        if self.participant.payoff is None:
            self.participant.set_payoff()
        return {
            'payoff': currency(self.participant.payoff),
            'rejected': True if self.match.decision == 'Reject' else False,
            'agent': True if self.participant.index_among_participants_in_match == 2 else False
        }


class ExperimenterPage(ExperimenterMixIn, ptree.views.ExperimenterPage):
    pass


def pages():
    return [
        Introduction,
        Offer,
        Accept,
        WorkEffort,
        Results
    ]