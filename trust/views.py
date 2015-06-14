# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range

from ._builtin import Page, WaitPage
from . import models
from .models import Constants


def vars_for_all_templates(self):
    return {'instructions': 'trust/Instructions.html', 'total_q': 1}


class Introduction(Page):

    template_name = 'global/Introduction.html'

    def vars_for_template(self):
        return {'amount_allocated': Constants.amount_allocated}


class Question1(Page):
    template_name = 'global/Question.html'
    form_model = models.Player
    form_fields = ['training_answer_x', 'training_answer_y']
    question = (
        'Suppose that participant A sent 20 points to participant B. '
        'Having received the tripled amount, participant B sent 50 points to '
        'participant A. In the end, how many points would participant A and B '
        'have?'
    )

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {'num_q': 1, 'question': self.question}


class Feedback(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {
            'num_q': 1,
        }



class Send(Page):

    """This page is only for P1
    P1 sends amount (all, some, or none) to P2
    This amount is tripled by experimenter,
    i.e if sent amount by P1 is 5, amount received by P2 is 15"""

    form_model = models.Group
    form_fields = ['sent_amount']

    def is_displayed(self):
        return self.player.id_in_group == 1



class SendBack(Page):

    """This page is only for P2
    P2 sends back some amount (of the tripled amount received) to P1"""

    form_model = models.Group
    form_fields = ['sent_back_amount']

    def is_displayed(self):
        return self.player.id_in_group == 2

    def vars_for_template(self):
        tripled_amount = self.group.sent_amount * Constants.multiplication_factor

        return {'amount_allocated': Constants.amount_allocated,
                'tripled_amount': tripled_amount,
                'prompt':
                'Please enter a number from 0 to %s:' % tripled_amount}

    def sent_back_amount_max(self):
        return self.group.sent_amount * Constants.multiplication_factor


class ResultsWaitPage(WaitPage):


    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):

    """This page displays the earnings of each player"""

    def vars_for_template(self):
        tripled_amount = self.group.sent_amount * Constants.multiplication_factor

        return {'amount_allocated': Constants.amount_allocated,
                'result': self.player.payoff - Constants.bonus,
                'tripled_amount': self.group.sent_amount * Constants.multiplication_factor
                }


page_sequence =  [
        Introduction,
        Question1,
        Feedback,
        Send,
        WaitPage,
        SendBack,
        ResultsWaitPage,
        Results,
    ]
