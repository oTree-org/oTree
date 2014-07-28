# -*- coding: utf-8 -*-
import bargaining.forms as forms
from bargaining.utilities import Page, MatchWaitPage, SubsessionWaitPage
from ptree.common import currency

class Introduction(Page):

    template_name = 'bargaining/Introduction.html'

    def variables_for_template(self):
        return {
            'amount_shared': currency(self.treatment.amount_shared),
        }


class Request(Page):

    template_name = 'bargaining/Request.html'

    def get_form_class(self):
        return forms.RequestForm

    def variables_for_template(self):
        return {
            'amount_shared': currency(self.treatment.amount_shared),
        }


class ResultsWaitPage(MatchWaitPage):

    def action(self):
        for p in self.match.participants():
            p.set_payoff()

class Results(Page):

    template_name = 'bargaining/Results.html'

    def variables_for_template(self):
        return {
            'payoff': currency(self.participant.payoff),
            'request_amount': currency(self.participant.request_amount),
            'other_request': currency(self.participant.other_participant().request_amount)
        }


def pages():
    return [
        Introduction,
        Request,
        ResultsWaitPage,
        Results
    ]