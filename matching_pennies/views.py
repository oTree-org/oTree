# -*- coding: utf-8 -*-
import matching_pennies.forms as forms
from matching_pennies._builtin import Page, MatchWaitPage, SubsessionWaitPage
from otree.common import Money, money_range

def variables_for_all_templates(self):
    return {
        'round_number': self.subsession.round_number,
        'role': self.player.role()
    }


class Choice(Page):

    template_name = 'matching_pennies/Choice.html'
    form_class = forms.PennySideForm

    def variables_for_template(self):
        return {
            'initial_amount': self.treatment.initial_amount,
            'winner_amount': self.treatment.initial_amount * 2,
            'loser_amount': Money(0)
        }


class ResultsWaitPage(MatchWaitPage):

    def after_all_players_arrive(self):
        self.match.set_payoffs()

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
