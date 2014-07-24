# -*- coding: utf-8 -*-
import ptree.views
import ptree.views.concrete
import matrix_symmetric.forms as forms
from matrix_symmetric.utilities import ParticipantMixIn, MatchMixIn, SubsessionMixIn
from ptree.common import currency


class Decision(ParticipantMixIn, ptree.views.Page):

    template_name = 'matrix_symmetric/Decision.html'

    def get_form_class(self):
        return forms.DecisionForm

    def variables_for_template(self):
        return {
            'self_A_other_A': currency(self.treatment.self_A_other_A),
            'self_A_other_B': currency(self.treatment.self_A_other_B),
            'self_B_other_A': currency(self.treatment.self_B_other_A),
            'self_B_other_B': currency(self.treatment.self_B_other_B),
        }


class ResultsCheckpoint(MatchMixIn, ptree.views.MatchCheckpoint):

    def action(self):
        for p in self.match.participants():
            p.set_payoff()

    def wait_page_body_text(self):
        return "Waiting for the other participant."


class Results(ParticipantMixIn, ptree.views.Page):

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


class ExperimenterPage(SubsessionMixIn, ptree.views.ExperimenterPage):
    pass


def pages():
    return [
        Decision,
        ResultsCheckpoint,
        Results
    ]