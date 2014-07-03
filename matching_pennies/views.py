# -*- coding: utf-8 -*-
import ptree.views
import ptree.views.concrete
import matching_pennies.forms as forms
from matching_pennies.utilities import ParticipantMixin, ExperimenterMixin
from ptree.common import currency


class Choice(ParticipantMixin, ptree.views.Page):

    template_name = 'matching_pennies/Choice.html'
    form_class = forms.PennySideForm

    def variables_for_template(self):
        return {'role': self.participant.role(),
                'initial_amount': currency(self.treatment.initial_amount),
                'winner_amount': currency(self.treatment.initial_amount * 2),
                'loser_amount': currency(0)}


class Results(ParticipantMixin, ptree.views.Page):

    template_name = 'matching_pennies/Results.html'

    def show_skip_wait(self):
        if self.participant.other_participant().penny_side:
            return self.PageActions.show
        else:
            return self.PageActions.wait

    def wait_page_body_text(self):
        return "Waiting for the other player to select heads or tails."

    def variables_for_template(self):
        if self.participant.payoff is None:
            self.participant.set_payoff()

        return {'my_choice': self.participant.penny_side,
                'other_choice': self.participant.other_participant().penny_side,
                'payoff': currency(self.participant.payoff),
                'role': self.participant.role()}


class ExperimenterPage(ExperimenterMixin, ptree.views.ExperimenterPage):

    pass


def pages():

    return [Choice,
            Results]
