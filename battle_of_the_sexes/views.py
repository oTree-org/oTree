# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants

def variables_for_all_templates(self):

    return {'total_q': 1,
            'total_rounds': Constants.number_of_rounds,
            'round_number': self.subsession.round_number,
            'role': self.player.role()}


class Introduction(Page):

    template_name = 'battle_of_the_sexes/Introduction.html'

    def participate_condition(self):
        return self.subsession.round_number == 1


class Question1(Page):

    template_name = 'battle_of_the_sexes/Question.html'

    def participate_condition(self):
        return self.subsession.round_number == 1

    form_model = models.Player
    form_fields = ['training_question_1_husband','training_question_1_wife']

    def variables_for_template(self):
        return {'num_q': 1}


class Feedback1(Page):

    template_name = 'battle_of_the_sexes/Feedback.html'

    def variables_for_template(self):
        return {
            'num_q': 1,

            'is_answer_husband_correct': self.player.is_training_question_1_husband_correct(),
            'answer_husband': self.player.training_question_1_husband,

            'is_answer_wife_correct': self.player.is_training_question_1_wife_correct(),
            'answer_wife': self.player.training_question_1_wife
        }


class Decide(Page):

    def participate_condition(self):
        return True

    template_name = 'battle_of_the_sexes/Decide.html'

    form_model = models.Player
    form_fields = ['decision']

    def variables_for_template(self):
        return {'role': self.player.role(),
                'fbl_husband_amt': Constants.football_husband_amount,
                'fbl_wife_amt': Constants.football_wife_amount,
                'fbl_opr_amt': Constants.mismatch_amount,
                'opr_husband_amt': Constants.opera_husband_amount,
                'opr_wife_amt': Constants.opera_wife_amount}


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()

    def body_text(self):
        return "Waiting for the other participant."


class Results(Page):

    def participate_condition(self):
        return True

    template_name = 'battle_of_the_sexes/Results.html'

    def variables_for_template(self):
        return {'role': self.player.role(),
                'decision': self.player.decision,
                'other_decision': self.player.other_player().decision,
                'payoff': self.player.payoff,
                'total_payoff': self.player.payoff + 10}


def pages():

    return [Introduction,
            Question1,
            Feedback1,
            Decide,
            ResultsWaitPage,
            Results]
