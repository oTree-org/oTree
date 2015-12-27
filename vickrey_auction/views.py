# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants


def vars_for_all_templates(self):

    return {'total_q': 1
            # 'total_rounds': Constants.num_rounds,
            # 'round_number': self.subsession.round_number
            }


class Introduction(Page):
    pass

class Question(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

    form_model = models.Player
    form_fields = ['training_question_1_my_payoff']

    def vars_for_template(self):
        return {'num_q': 1}


class Feedback1(Page):

    template_name = 'vickrey_auction/Feedback.html'

    def vars_for_template(self):
        return {
            'num_q': 1
        }


class Bid(Page):

    form_model = models.Player
    form_fields = ['bid_amount']


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_winner()
        self.group.set_payoffs()


class Results(Page):
    pass


page_sequence = [Introduction,
            Question,
            Feedback1,
            Bid,
            ResultsWaitPage,
            Results]
