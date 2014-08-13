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
        print 1/0
        self.match.set_payoffs()

class Results(Page):

    template_name = 'bargaining/Results.html'

    def variables_for_template(self):
        return {
            'payoff': self.player.payoff,
            'request_amount': self.player.request_amount,
            'other_request': self.player.other_player().request_amount
        }


def pages():
    return [
        Introduction,
        Request,
        ResultsWaitPage,
        Results
    ]