# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants


def vars_for_all_templates(self):

    return {'total_q': 1,
            'total_rounds': Constants.num_rounds,
            'round_number': self.subsession.round_number}


class Introduction(Page):

    template_name = 'stag_hunt/Introduction.html'

    def is_displayed(self):
        return self.subsession.round_number == 1


class Question1(Page):

    template_name = 'stag_hunt/Question.html'

    def is_displayed(self):
        return self.subsession.round_number == 1

    form_model = models.Player
    form_fields = [
        'training_question_1_my_payoff','training_question_1_other_payoff'
    ]

    def vars_for_template(self):
        return {'num_q': 1}


class Feedback1(Page):

    template_name = 'stag_hunt/Feedback.html'

    def vars_for_template(self):
        return {
            'num_q': 1,

            # 'is_training_question_1_my_payoff_correct': self.player.is_training_question_1_my_payoff_correct(),
            # 'answer_you': self.player.training_question_1_my_payoff,
            #
            # 'is_training_question_1_other_payoff_correct': self.player.is_training_question_1_other_payoff_correct(),
            # 'answer_other': self.player.training_question_1_other_payoff,
        }


class Decide(Page):

    def is_displayed(self):
        return True

    template_name = 'stag_hunt/Decide.html'

    form_model = models.Player
    form_fields = ['decision']

    def vars_for_template(self):
        return {'player_index': self.player.id_in_group,
                'stag_stag': Constants.stag_stag_amount,
                'stag_hare': Constants.stag_hare_amount,
                'hare_stag': Constants.hare_stag_amount,
                'hare_hare': Constants.hare_hare_amount}


class ResultsWaitPage(WaitPage):



    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_payoff()

    def body_text(self):
        return "Waiting for the other participant."


class Results(Page):

    def is_displayed(self):
        return True

    template_name = 'stag_hunt/Results.html'

    def vars_for_template(self):

        return {
             'total_payoff': self.player.payoff + Constants.fixed_pay}


page_sequence = [Introduction,
            Question1,
            Feedback1,
            Decide,
            ResultsWaitPage,
            Results]
