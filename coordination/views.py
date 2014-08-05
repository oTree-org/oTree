# -*- coding: utf-8 -*-
import coordination.forms as forms
from coordination.utilities import Page, MatchWaitPage, SubsessionWaitPage
from ptree.common import Money, money_range


class Introduction(Page):

    def participate_condition(self):
        return True

    template_name = 'coordination/Introduction.html'

    def variables_for_template(self):
        return {
            'match_amount': self.treatment.match_amount,
            'mismatch_amount': self.treatment.mismatch_amount,
        }


class Choice(Page):

    def participate_condition(self):
        return True

    template_name = 'coordination/Choice.html'

    def get_form_class(self):
        return forms.ChoiceForm


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
            'payoff': self.participant.payoff,
            'choice': self.participant.choice,
            'other_choice': self.participant.other_participant().choice
        }


def pages():
    return [
        Introduction,
        Choice,
        ResultsWaitPage,
        Results
    ]