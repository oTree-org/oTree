# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Money, money_range
from .models import Constants

def variables_for_all_templates(self):
    return dict(instructions='trust/Instructions.html', total_q=1)


class Introduction(Page):

    template_name = 'global/Introduction.html'

    def variables_for_template(self):
        return {'amount_allocated': Constants.amount_allocated}


class Question1(Page):
    template_name = 'global/Question.html'
    form_model = models.Player
    form_fields = 'training_answer_x', 'training_answer_y'
    question = '''Suppose that participant A sent 20 points to participant B. Having received the tripled amount, participant B sent 50 points to participant A. In the end, how many points would participant A and B have?'''

    def participate_condition(self):
        return self.subsession.round_number == 1

    def variables_for_template(self):
        return dict(num_q=1, question=self.question)


class Feedback1(Page):
    template_name = 'trust/Feedback.html'

    def participate_condition(self):
        return self.subsession.round_number == 1

    def variables_for_template(self):
        return dict(
            num_q=1, x=self.player.training_answer_x,
            y=self.player.training_answer_y)


class Question2(Page):
    template_name = 'global/Question.html'
    form_model = models.Player
    form_fields = 'feedback',

    def participate_condition(self):
        return self.subsession.round_number == 1

    def variables_for_template(self):
        return dict(
            num_q=1,
            title='Questionnaire',
            question='How well do you think this sample game was implemented?')


class Send(Page):

    """This page is only for P1
    P1 sends amount (all, some, or none) to P2
    This amount is tripled by experimenter,
    i.e if sent amount by P1 is 5, amount received by P2 is 15"""

    template_name = 'trust/Send.html'

    form_model = models.Group
    form_fields = ['sent_amount']

    def participate_condition(self):
        return self.player.id_in_group == 1

    def variables_for_template(self):
        return {'amount_allocated': Constants.amount_allocated}


class WaitPage(WaitPage):

    scope = models.Group

    def body_text(self):
        return 'Waiting for other participant to decide.'


class SendBack(Page):

    """This page is only for P2
    P2 sends back some amount (of the tripled amount received) to P1"""

    template_name = 'trust/SendBack.html'

    form_model = models.Group
    form_fields = ['sent_back_amount']

    def participate_condition(self):
        return self.player.id_in_group == 2

    def variables_for_template(self):
        tripled_amount = self.group.sent_amount * Constants.multiplication_factor

        return {'amount_allocated': Constants.amount_allocated,
                'sent_amount': self.group.sent_amount,
                'tripled_amount': tripled_amount,
                'prompt':
                'Please enter a number from 0 to %s:' % tripled_amount}


class ResultsWaitPage(WaitPage):

    scope = models.Group

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):

    """This page displays the earnings of each player"""

    template_name = 'trust/Results.html'

    def variables_for_template(self):
        tripled_amount = self.group.sent_amount * Constants.multiplication_factor

        return {'amount_allocated': Constants.amount_allocated,
                'sent_amount': self.group.sent_amount,
                'tripled_amount': tripled_amount,
                'sent_back_amount': self.group.sent_back_amount,
                'role': self.player.role(),
                'bonus': Constants.bonus,
                'result': self.player.points - Constants.bonus,
                'total': self.player.points}


def pages():

    return [Introduction,
            Question1,
            Feedback1,
            Send,
            WaitPage,
            SendBack,
            ResultsWaitPage,
            Results,
            Question2,
            ]
