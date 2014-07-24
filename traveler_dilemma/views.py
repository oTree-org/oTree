# -*- coding: utf-8 -*-
import ptree.views
import ptree.views.concrete
import traveler_dilemma.forms as forms
from traveler_dilemma.utilities import ParticipantMixIn, MatchMixIn, SubsessionMixIn
from django.utils.translation import ugettext as _
from django.conf import settings
from ptree.common import currency


class Introduction(ParticipantMixIn, ptree.views.Page):

    template_name = 'traveler_dilemma/Introduction.html'

    def variables_for_template(self):
        return {
            'max_amount': currency(self.treatment.max_amount),
            'min_amount': currency(self.treatment.min_amount),
            'reward': currency(self.treatment.reward),
            'penalty': currency(self.treatment.penalty),
        }


class Claim(ParticipantMixIn, ptree.views.Page):

    template_name = 'traveler_dilemma/Claim.html'

    def get_form_class(self):
        return forms.ClaimForm

class ResultsCheckpoint(MatchMixIn, ptree.views.MatchCheckpoint):

    def action(self):
        for p in self.match.participants():
            p.set_payoff()


class Results(ParticipantMixIn, ptree.views.Page):

    template_name = 'traveler_dilemma/Results.html'

    def variables_for_template(self):
        return {
            'claim': currency(self.participant.claim),
            'other_claim': currency(self.participant.other_participant().claim),
            'payoff': currency(self.participant.payoff)
        }


def pages():
    return [
        Introduction,
        Claim,
        ResultsCheckpoint,
        Results
    ]
