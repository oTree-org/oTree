# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants

def vars_for_all_templates(self):

    return {'total_q': 1}


class Introduction(Page):

    pass


class Question1(Page):

    template_name = 'beauty/Question.html'

    def is_displayed(self):
        return self.subsession.round_number == 1

    form_model = models.Player
    form_fields = ['training_question_1_win_pick',
                   'training_question_1_my_payoff']

    def vars_for_template(self):
        return {'num_q': 1}


class Feedback1(Page):

    template_name = 'beauty/Feedback.html'

    def vars_for_template(self):
        return {
            'num_q': 1,

        }



class Guess(Page):

    form_model = models.Player
    form_fields = ['guess_value']


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()

    body_text = "Waiting for the other participants."



class Results(Page):

    def vars_for_template(self):
        other_guesses = []
        winners_cnt = int(self.player.is_winner)
        for p in self.player.get_others_in_group():
            other_guesses.append(p.guess_value)
            winners_cnt += int(p.is_winner)

        return {
            'other_guesses': other_guesses,
            'other_guesses_count': len(other_guesses),
            'two_third_average': round(self.group.two_third_guesses, 4),
            'winners_cnt': winners_cnt,
            'total_payoff': self.player.payoff + Constants.fixed_pay,
        }


page_sequence = [Introduction,
            Question1,
            Feedback1,
            Guess,
            ResultsWaitPage,
            Results]
