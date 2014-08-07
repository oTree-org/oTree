# -*- coding: utf-8 -*-
import matching_pennies.forms as forms
from matching_pennies.utilities import Page, MatchWaitPage, SubsessionWaitPage
from ptree.common import Money, money_range


class Choice(Page):

    template_name = 'matching_pennies/Choice.html'
    form_class = forms.PennySideForm

    def variables_for_template(self):
        return {'role': self.participant.role(),
                'initial_amount': self.treatment.initial_amount,
                'winner_amount': self.treatment.initial_amount * 2,
                'loser_amount': Money(0)}


class ResultsWaitPage(MatchWaitPage):

    def action(self):
        for p in self.match.participants():
            p.set_payoff()

    def body_text(self):
        return "Waiting for the other player to select heads or tails."

class Results(Page):

    template_name = 'matching_pennies/Results.html'

    def variables_for_template(self):

        return {'my_choice': self.participant.penny_side,
                'other_choice': self.participant.other_participant().penny_side,
                'payoff': self.participant.payoff,
                'role': self.participant.role()}

def pages():

    return [Choice,
            ResultsWaitPage,
            Results]
