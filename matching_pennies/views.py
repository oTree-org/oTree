# -*- coding: utf-8 -*-
import ptree.views
import ptree.views.concrete
import matching_pennies.forms as forms
from matching_pennies.utilities import ParticipantMixIn, MatchMixIn, SubsessionMixIn
from ptree.common import currency


class Choice(ParticipantMixIn, ptree.views.Page):

    template_name = 'matching_pennies/Choice.html'
    form_class = forms.PennySideForm

    def variables_for_template(self):
        return {'role': self.participant.role(),
                'initial_amount': currency(self.treatment.initial_amount),
                'winner_amount': currency(self.treatment.initial_amount * 2),
                'loser_amount': currency(0)}


class ResultsCheckpoint(MatchMixIn, ptree.views.MatchCheckpoint):

    def action(self):
        for p in self.match.participants():
            p.set_payoff()

    def wait_page_body_text(self):
        return "Waiting for the other player to select heads or tails."

class Results(ParticipantMixIn, ptree.views.Page):

    template_name = 'matching_pennies/Results.html'

    def variables_for_template(self):

        return {'my_choice': self.participant.penny_side,
                'other_choice': self.participant.other_participant().penny_side,
                'payoff': currency(self.participant.payoff),
                'role': self.participant.role()}

def pages():

    return [Choice,
            ResultsCheckpoint,
            Results]
