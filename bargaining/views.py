# -*- coding: utf-8 -*-
import bargaining.forms as forms
from bargaining.utilities import Page, MatchWaitPage, SubsessionWaitPage
from otree.common import Money, money_range

class Introduction(Page):

    template_name = 'bargaining/Introduction.html'

    def variables_for_template(self):
        return {
            'amount_shared': self.treatment.amount_shared,
        }


class Request(Page):

    template_name = 'bargaining/Request.html'

    def get_form_class(self):
        return forms.RequestForm

    def variables_for_template(self):
        return {
            'amount_shared': self.treatment.amount_shared,
        }


class ResultsWaitPage(MatchWaitPage):

    def action(self):
        for p in self.match.participants():
            p.set_payoff()

class Results(Page):

    template_name = 'bargaining/Results.html'

    def variables_for_template(self):
        return {
            'payoff': self.participant.payoff,
            'request_amount': self.participant.request_amount,
            'other_request': self.participant.other_participant().request_amount
        }


def pages():
    return [
        Introduction,
        Request,
        ResultsWaitPage,
        Results
    ]