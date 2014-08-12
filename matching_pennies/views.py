# -*- coding: utf-8 -*-
import matching_pennies.forms as forms
from matching_pennies.utilities import Page, MatchWaitPage, SubsessionWaitPage
from otree.common import Money, money_range


class Choice(Page):

    template_name = 'matching_pennies/Choice.html'
    form_class = forms.PennySideForm

    def variables_for_template(self):
        return {'role': self.player.role(),
                'initial_amount': self.treatment.initial_amount,
                'winner_amount': self.treatment.initial_amount * 2,
                'loser_amount': Money(0)}


class ResultsWaitPage(MatchWaitPage):

    def action(self):
        for p in self.match.players():
            p.set_payoff()

    def body_text(self):
        return "Waiting for the other player to select heads or tails."

class Results(Page):

    template_name = 'matching_pennies/Results.html'

    def variables_for_template(self):

        return {'my_choice': self.player.penny_side,
                'other_choice': self.player.other_player().penny_side,
                'payoff': self.player.payoff,
                'role': self.player.role()}

def pages():

    return [Choice,
            ResultsWaitPage,
            Results]
