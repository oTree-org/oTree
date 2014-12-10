# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants

def variables_for_all_templates(self):
    return {'total_q':1,
            'instructions':'bargaining/Instructions.html',
            'amount_shared': Constants.amount_shared}


class Introduction(Page):

    template_name = 'global/Introduction.html'

    def variables_for_template(self):
        return {
            'amount_shared': Constants.amount_shared,
        }


class Question1(Page):
    template_name = 'global/Question.html'
    form_model = models.Player
    form_fields = ['training_amount_mine', 'training_amount_other']

    def participate_condition(self):
        return self.subsession.round_number == 1

    def variables_for_template(self):
        return {'num_q': 1, 'question': '''Suppose that you demanded 55 points and the other participant demanded 80 points.
            What would you and the other participant get respectively?'''}


class Feedback1(Page):
    template_name = 'bargaining/Feedback.html'

    def participate_condition(self):
        return self.subsession.round_number == 1

    def variables_for_template(self):
        return {
            'num_q': 1,
            'mine':self.player.training_amount_mine,
            'other': self.player.training_amount_other
        }


class Request(Page):

    template_name = 'bargaining/Request.html'

    form_model = models.Player
    form_fields = ['request_amount']

    def variables_for_template(self):
        return {
            'amount_shared': Constants.amount_shared,
        }


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):

    template_name = 'bargaining/Results.html'

    def variables_for_template(self):
        return {
            'earn': self.player.payoff - Constants.bonus,
            'points': self.player.payoff,
            'request_amount': self.player.request_amount,
            'other_request': self.player.other_player().request_amount,
            'sum': self.player.request_amount + self.player.other_player(
                ).request_amount
        }




def pages():
    return [
        Introduction,
        Question1,
        Feedback1,
        Request,
        ResultsWaitPage,
        Results,
    ]
