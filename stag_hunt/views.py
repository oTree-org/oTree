# -*- coding: utf-8 -*-
import ptree.views
import ptree.views.concrete
import stag_hunt.forms as forms
from stag_hunt.utilities import ParticipantMixIn, MatchMixIn
from ptree.common import currency


class Decide(ParticipantMixIn, ptree.views.Page):

    def participate_condition(self):
        return True

    template_name = 'stag_hunt/Decide.html'

    def get_form_class(self):
        return forms.DecisionForm

    def variables_for_template(self):
        return {
            'stag_stag': currency(self.treatment.stag_stag_amount),
            'stag_hare': currency(self.treatment.stag_hare_amount),
            'hare_stag': currency(self.treatment.hare_stag_amount),
            'hare_hare': currency(self.treatment.hare_hare_amount),
        }


class ResultsCheckpoint(MatchMixIn, ptree.views.MatchCheckpoint):

    def action(self):
        for p in self.match.participants():
            p.set_payoff()

    def wait_page_body_text(self):
        return "Waiting for the other participant."


class Results(ParticipantMixIn, ptree.views.Page):

    def participate_condition(self):
        return True

    template_name = 'stag_hunt/Results.html'

    def variables_for_template(self):
        if self.participant.payoff is None:
            self.participant.set_payoff()

        return {
            'payoff': currency(self.participant.payoff),
            'decision': self.participant.decision,
            'other_decision': self.participant.other_participant().decision,
        }


def pages():
    return [
        Decide,
        ResultsCheckpoint,
        Results
    ]