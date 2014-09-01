# -*- coding: utf-8 -*-
import guessing.forms as forms
from guessing._builtin import Page, SubsessionWaitPage


class Introduction(Page):

    template_name = 'guessing/Introduction.html'

    def variables_for_template(self):
        return {'players_count': len(self.player.other_players_in_subsession()),
                'winner_payoff': self.treatment.winner_payoff}


class Guess(Page):

    template_name = 'guessing/Guess.html'

    def get_form_class(self):
        return forms.GuessForm


class Results(Page):

    template_name = 'guessing/Results.html'

    def variables_for_template(self):
        other_guesses = [p.guess_value for p in self.player.other_players_in_subsession()]

        return {'guess_value': self.player.guess_value,
                'other_guesses': other_guesses,
                'other_guesses_count': len(other_guesses),
                'two_third_average': round(self.subsession.two_third_guesses, 4),
                'players': self.subsession.players,
                'is_winner': self.player.is_winner,
                'payoff': self.player.payoff}


class ResultsWaitPage(SubsessionWaitPage):

    def after_all_players_arrive(self):
        self.subsession.set_payoffs()


def pages():

    return [Introduction,
            Guess,
            ResultsWaitPage,
            Results]
