# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Money, money_range
from .models import Constants

class Introduction(Page):

    template_name = 'guessing/Introduction.html'

    def variables_for_template(self):
        return {'players_count': len(self.player.get_others_in_subsession()),
                'winner_payoff': Constants.winner_payoff}


class Guess(Page):

    template_name = 'guessing/Guess.html'

    form_model = models.Player
    form_fields = ['guess_value']


class Results(Page):

    template_name = 'guessing/Results.html'

    def variables_for_template(self):
        other_guesses = [p.guess_value for p in self.player.get_others_in_subsession()]

        return {'guess_value': self.player.guess_value,
                'other_guesses': other_guesses,
                'other_guesses_count': len(other_guesses),
                'two_third_average': round(self.group.two_third_guesses, 4),
                'players': self.subsession.get_players(),
                'is_winner': self.player.is_winner,
                'best_guess': self.group.best_guess,
                'payoff': self.player.payoff}


class ResultsWaitPage(WaitPage):

    scope = models.Group

    def after_all_players_arrive(self):
        self.group.set_payoffs()


def pages():

    return [Introduction,
            Guess,
            ResultsWaitPage,
            Results]
