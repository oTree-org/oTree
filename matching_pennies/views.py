# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants

def vars_for_all_templates(self):

    return {'total_q': 1,
            'total_rounds': Constants.num_rounds,
            'round_number': self.subsession.round_number,
            'role': self.player.role()}


class Introduction(Page):

    template_name = 'matching_pennies/Introduction.html'

    def participate_condition(self):
        return self.subsession.round_number == 1


class Question1(Page):

    template_name = 'matching_pennies/Question.html'

    def participate_condition(self):
        return self.subsession.round_number == 1

    form_model = models.Player
    form_fields = ['training_question_1']

    def vars_for_template(self):
        return {'num_q': 1}


class Feedback1(Page):

    template_name = 'matching_pennies/Feedback.html'

    def participate_condition(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {'num_q': 1,
                'question': 'Suppose Player 1 picked "Heads" and Player 2 guessed "Tails". Which of the following will be the result of that round?',
                'answer': self.player.training_question_1,
                'correct': Constants.training_1_correct,
                'explanation': 'Player 1 gets 100 points, Player 2 gets 0 points',
                'is_correct': self.player.is_training_question_1_correct()}


class Choice(Page):

    template_name = 'matching_pennies/Choice.html'

    form_model = models.Player
    form_fields = ['penny_side']


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()

    def body_text(self):
        return "Waiting for your opponent."


class Results(Page):

    template_name = 'matching_pennies/Results.html'

    def vars_for_template(self):
        return {'my_choice': self.player.penny_side,
                'other_choice': self.player.other_player().penny_side,
                'my_points': self.player.payoff,
                'other_points': self.player.other_player().payoff,
                'my_payoff': self.player.payoff,
                'other_payoff': self.player.other_player().payoff}


class ResultsSummary(Page):

    template_name = 'matching_pennies/ResultsSummary.html'

    def participate_condition(self):
        return self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):
        player_in_all_rounds = self.player.in_all_rounds()
        total_payoff = sum([p.payoff for p in player_in_all_rounds])
        base_points = 50

        return {'player_in_all_rounds': player_in_all_rounds,
                'payoff': self.player.payoff,
                'is_winner': self.player.is_winner,
                'total_payoff': total_payoff,
                'base_points': base_points,
                'total_plus_base': total_payoff + base_points}


def pages():

    return [Introduction,
            Question1,
            Feedback1,
            Choice,
            ResultsWaitPage,
            Results,
            ResultsSummary]
