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

    def is_displayed(self):
        return self.subsession.round_number == 1


class Question(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

    form_model = models.Player
    form_fields = ['training_question_1']

    def vars_for_template(self):
        return {'num_q': 1}


class Feedback1(Page):

    template_name = 'matching_pennies/Feedback.html'

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {'num_q': 1,
               # 'question': 'Suppose Player 1 picked "Heads" and Player 2 guessed "Tails". Which of the following will be the result of that round?',
               #  'answer': self.player.training_question_1,
               #  'correct': Constants.training_1_correct,
              #  'explanation': 'Player 1 gets 100 points, Player 2 gets 0 points',
              #  'is_correct': self.player.is_training_question_1_correct()
        }


class Choice(Page):

    form_model = models.Player
    form_fields = ['penny_side']


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()

    body_text = "Waiting for your opponent."


class Results(Page):
    pass


class ResultsSummary(Page):

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):
        player_in_all_rounds = self.player.in_all_rounds()
        total_payoff = sum([p.payoff for p in player_in_all_rounds])


        return {'player_in_all_rounds': player_in_all_rounds,
                'total_payoff': total_payoff,
                'total_plus_base': total_payoff + Constants.base_points}


page_sequence = [Introduction,
            Question,
            Feedback1,
            Choice,
            ResultsWaitPage,
            Results,
            ResultsSummary]
