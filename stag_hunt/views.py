# -*- coding: utf-8 -*-
import stag_hunt.forms as forms
from stag_hunt.utilities import Page, MatchWaitPage, SubsessionWaitPage
from ptree.common import Money, money_range


class Decide(Page):

    def participate_condition(self):
        return True

    template_name = 'stag_hunt/Decide.html'

    def get_form_class(self):
        return forms.DecisionForm

    def variables_for_template(self):
        return {
            'stag_stag': self.treatment.stag_stag_amount,
            'stag_hare': self.treatment.stag_hare_amount,
            'hare_stag': self.treatment.hare_stag_amount,
            'hare_hare': self.treatment.hare_hare_amount,
        }


class ResultsWaitPage(MatchWaitPage):

    def action(self):
        for p in self.match.participants():
            p.set_payoff()

    def body_text(self):
        return "Waiting for the other participant."


class Results(Page):

    def participate_condition(self):
        return True

    template_name = 'stag_hunt/Results.html'

    def variables_for_template(self):

        return {
            'payoff': self.participant.payoff,
            'decision': self.participant.decision,
            'other_decision': self.participant.other_participant().decision,
        }


def pages():
    return [
        Decide,
        ResultsWaitPage,
        Results
    ]