# -*- coding: utf-8 -*-
import ptree.views
import ptree.views.concrete
import traveler_dilemma.forms as forms
from traveler_dilemma.utilities import ParticipantMixin, ExperimenterMixin
from django.utils.translation import ugettext as _
from django.conf import settings
from ptree.common import currency


class Introduction(ParticipantMixin, ptree.views.Page):

    def show_skip_wait(self):
        return self.PageActions.show

    template_name = 'traveler_dilemma/Introduction.html'

    def variables_for_template(self):
        return {
            'max_amount': currency(self.treatment.max_amount),
            'min_amount': currency(self.treatment.min_amount),
            'reward': currency(self.treatment.reward),
            'penalty': currency(self.treatment.penalty),
        }


class Claim(ParticipantMixin, ptree.views.Page):

    def show_skip_wait(self):
        return self.PageActions.show

    template_name = 'traveler_dilemma/Claim.html'

    def get_form_class(self):
        return forms.ClaimForm


class Results(ParticipantMixin, ptree.views.Page):

    def show_skip_wait(self):
        if self.participant.other_participant().claim:
            return self.PageActions.show
        else:
            return self.PageActions.wait

    template_name = 'traveler_dilemma/Results.html'

    def variables_for_template(self):
        if self.participant.payoff is None:
            self.participant.set_payoff()
        return {
            'claim': currency(self.participant.claim),
            'other_claim': currency(self.participant.other_participant().claim),
            'payoff': currency(self.participant.payoff)
        }


def pages():
    return [
        Introduction,
        Claim,
        Results
    ]
