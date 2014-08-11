# -*- coding: utf-8 -*-
import guessing.forms as forms
from guessing.utilities import Page, MatchWaitPage, SubsessionWaitPage
from otree.common import Money, money_range


class Introduction(Page):

    template_name = 'guessing/Introduction.html'


class Guess(Page):

    template_name = 'guessing/Guess.html'

    def get_form_class(self):
        return forms.GuessForm


class Results(Page):

    template_name = 'guessing/Results.html'

    def variables_for_template(self):
        return {
            'payoff': self.participant.payoff,
            'guess_value': self.participant.guess_value,
            'two_third_average': self.subsession.two_third_guesses,
            'is_winner': self.participant.is_winner,
        }

class ResultsWaitPage(SubsessionWaitPage):

    def action(self):
        self.subsession.choose_winner()

        for p in self.subsession.participants():
            p.set_payoff()

def pages():
    return [
        Introduction,
        Guess,
        ResultsWaitPage,
        Results
    ]