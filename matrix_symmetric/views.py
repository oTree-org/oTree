# -*- coding: utf-8 -*-
import ptree.views
import ptree.views.concrete
import matrix_symmetric.forms as forms
from matrix_symmetric.utilities import ParticipantMixIn, ExperimenterMixIn
from ptree.common import currency


class Decision(ParticipantMixIn, ptree.views.Page):

    def show_skip_wait(self):
        return self.PageActions.show

    template_name = 'matrix_symmetric/Decision.html'

    def get_form_class(self):
        return forms.DecisionForm

    def variables_for_template(self):
        return {
            'self_1_other_1': self.treatment.self_1_other_1,
            'self_1_other_2': self.treatment.self_1_other_2,
            'self_2_other_1': self.treatment.self_2_other_1,
            'self_2_other_2': self.treatment.self_2_other_2,
        }


class Results(ParticipantMixIn, ptree.views.Page):

    def show_skip_wait(self):
        if self.participant.other_participant().decision:
            return self.PageActions.show
        else:
            return self.PageActions.wait

    template_name = 'matrix_symmetric/Results.html'

    def variables_for_template(self):

        if self.participant.payoff is None:
            self.participant.set_payoff()

        return {
            'payoff': currency(self.participant.payoff),
            'my_decision': self.participant.decision,
            'other_decision': self.participant.other_participant().decision,
            'same_decision': True if self.participant.decision == self.participant.other_participant().decision else False,
        }


class ExperimenterPage(ExperimenterMixIn, ptree.views.ExperimenterPage):
    pass


def pages():
    return [
        Decision,
        Results
    ]