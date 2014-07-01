# -*- coding: utf-8 -*-
import ptree.views
import ptree.views.concrete
import bargaining.forms as forms
from bargaining.utilities import ParticipantMixin
from ptree.common import currency


class Introduction(ParticipantMixin, ptree.views.Page):

    def show_skip_wait(self):
        return self.PageActions.show

    template_name = 'bargaining/Introduction.html'

    def variables_for_template(self):
        return {
            'amount_shared': currency(self.treatment.amount_shared),
        }


class Request(ParticipantMixin, ptree.views.Page):

    def show_skip_wait(self):
        return self.PageActions.show

    template_name = 'bargaining/Request.html'

    def get_form_class(self):
        return forms.RequestForm

    def variables_for_template(self):
        return {
            'amount_shared': currency(self.treatment.amount_shared),
        }


class Results(ParticipantMixin, ptree.views.Page):

    def show_skip_wait(self):
        if self.participant.other_participant().request_amount:
            return self.PageActions.show
        else:
            return self.PageActions.wait

    template_name = 'bargaining/Results.html'

    def variables_for_template(self):
        if self.participant.payoff is None:
            self.participant.set_payoff()
        return {
            'payoff': currency(self.participant.payoff),
            'request_amount': currency(self.participant.request_amount),
            'other_request': currency(self.participant.other_participant().request_amount)
        }


def pages():
    return [
        Introduction,
        Request,
        Results
    ]