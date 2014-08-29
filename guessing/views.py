# -*- coding: utf-8 -*-
import guessing.forms as forms
from guessing._builtin import Page, SubsessionWaitPage


class Introduction(Page):

    template_name = 'guessing/Introduction.html'

    def variables_for_template(self):
        return {'players_count': len(self.subsession.players),
                'winner_payoff': self.treatment.winner_payoff}


class Guess(Page):

    template_name = 'guessing/Guess.html'

    def get_form_class(self):
        return forms.GuessForm


class Results(Page):

    template_name = 'guessing/Results.html'

    def variables_for_template(self):
        return {'payoff': self.player.payoff,
                'guess_value': self.player.guess_value,
                'two_third_average': round(self.subsession.two_third_guesses, 4),
                'is_winner': self.player.is_winner}


class ResultsWaitPage(SubsessionWaitPage):

    def after_all_players_arrive(self):
        self.subsession.set_payoffs()


def pages():

    return [Introduction,
            Guess,
            ResultsWaitPage,
            Results]
