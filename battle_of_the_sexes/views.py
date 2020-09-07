# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants

def vars_for_all_templates(self):

    return {
            'total_q': 1,
            'total_rounds': Constants.num_rounds,
            'round_number': self.subsession.round_number,
            'role': self.player.role()
           }


class Introduction(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1


class Question1(Page):

    template_name = 'battle_of_the_sexes/Question.html'

    def is_displayed(self):
        return self.subsession.round_number == 1

    form_model = models.Player
    form_fields = ['training_question_1_husband','training_question_1_wife']

    def vars_for_template(self):
        return {'num_q': 1}


class Feedback1(Page):

    template_name = 'battle_of_the_sexes/Feedback.html'

    def vars_for_template(self):
        return {
            'num_q': 1,
               }


class Decide(Page):

    def is_displayed(self):
        return True

    form_model = models.Player
    form_fields = ['decision']

    def vars_for_template(self):
        return {#'role': self.player.role(),
                'fbl_husband_amt': Constants.football_husband_amount,
                'fbl_wife_amt': Constants.football_wife_amount,
                'fbl_opr_amt': Constants.mismatch_amount,
                'opr_husband_amt': Constants.opera_husband_amount,
                'opr_wife_amt': Constants.opera_wife_amount}


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()

    body_text = "Waiting for the other participant."


class Results(Page):

    def is_displayed(self):
        return True

    def vars_for_template(self):
        return {
            'total_payoff': self.player.payoff + Constants.fixed_pay
        }



page_sequence = [Introduction,
            Question1,
            Feedback1,
            Decide,
            ResultsWaitPage,
            Results]
