# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants

def vars_for_all_templates(self):
    return {'total_q':1,
            'instructions':'bargaining/Instructions.html',
            'amount_shared': Constants.amount_shared}


class Introduction(Page):

    template_name = 'global/Introduction.html'

    def vars_for_template(self):
        return {
            'amount_shared': Constants.amount_shared,
        }


class Question1(Page):
    template_name = 'global/Question.html'
    form_model = models.Player
    form_fields = ['training_amount_mine', 'training_amount_other']

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {'num_q': 1, 'question': '''Suppose that you demanded 55 points and the other participant demanded 80 points.
            What would you and the other participant get respectively?'''}


class Feedback(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {
            'num_q': 1,

        }


class Request(Page):

    form_model = models.Player
    form_fields = ['request_amount']

    def vars_for_template(self):
        return {
            'amount_shared': Constants.amount_shared,
        }


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):



    def vars_for_template(self):
        return {
                'sum':self.player.request_amount + self.player.other_player().request_amount,
                'earn':self.player.payoff - Constants.bonus

        }




page_sequence=[
        Introduction,
        Question1,
        Feedback,
        Request,
        ResultsWaitPage,
        Results,
    ]
