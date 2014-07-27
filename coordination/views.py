# -*- coding: utf-8 -*-
import coordination.forms as forms
from coordination.utilities import Page, MatchWaitPage, SubsessionWaitPage
from ptree.common import currency


class Choice(Page):

    def participate_condition(self):
        return True

    template_name = 'coordination/Choice.html'

    def get_form_class(self):
        return forms.ChoiceForm

    def variables_for_template(self):
        return {
            'match_amount': currency(self.treatment.match_amount),
            'mismatch_amount': currency(self.treatment.mismatch_amount),
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

    template_name = 'coordination/Results.html'

    def variables_for_template(self):
        return {
            'payoff': currency(self.participant.payoff),
            'choice': self.participant.choice,
            'other_choice': self.participant.other_participant().choice,
            'same_choice': True if self.participant.choice == self.participant.other_participant().choice else False
        }


def pages():
    return [
        Choice,
        ResultsWaitPage,
        Results
    ]