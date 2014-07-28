# -*- coding: utf-8 -*-
import traveler_dilemma.forms as forms
from traveler_dilemma.utilities import Page, MatchWaitPage, SubsessionWaitPage
from ptree.common import currency


class Introduction(Page):

    template_name = 'traveler_dilemma/Introduction.html'

    def variables_for_template(self):
        return {
            'max_amount': currency(self.treatment.max_amount),
            'min_amount': currency(self.treatment.min_amount),
            'reward': currency(self.treatment.reward),
            'penalty': currency(self.treatment.penalty),
        }


class Claim(Page):

    template_name = 'traveler_dilemma/Claim.html'

    def get_form_class(self):
        return forms.ClaimForm

class ResultsWaitPage(MatchWaitPage):

    def action(self):
        for p in self.match.participants():
            p.set_payoff()


class Results(Page):

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
        ResultsWaitPage,
        Results
    ]
