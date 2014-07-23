# -*- coding: utf-8 -*-
import ptree.views
import ptree.views.concrete
import bargaining.forms as forms
from bargaining.utilities import ParticipantMixIn, MatchMixIn
from ptree.common import currency


class Introduction(ParticipantMixIn, ptree.views.Page):

    template_name = 'bargaining/Introduction.html'

    def variables_for_template(self):
        return {
            'amount_shared': currency(self.treatment.amount_shared),
        }


class Request(ParticipantMixIn, ptree.views.Page):

    template_name = 'bargaining/Request.html'

    def get_form_class(self):
        return forms.RequestForm

    def variables_for_template(self):
        return {
            'amount_shared': currency(self.treatment.amount_shared),
        }


class ResultsCheckpoint(MatchMixIn, ptree.views.MatchCheckpoint):

    def action(self):
        for p in self.match.participants():
            p.set_payoff()

class Results(ParticipantMixIn, ptree.views.Page):

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
        ResultsCheckpoint,
        Results
    ]