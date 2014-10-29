# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Money, money_range
from .models import Constants


def variables_for_all_templates(self):

    return {'total_q': 1,
            'total_rounds': Constants.number_of_rounds,
            'round_number': self.subsession.round_number}


class Introduction(Page):

    template_name = 'private_value_auction/Introduction.html'


class QuestionOne(Page):

    template_name = 'private_value_auction/Question.html'

    def participate_condition(self):
        return self.subsession.round_number == 1

    form_model = models.Player
    form_fields = ['training_question_1_my_payoff']

    def variables_for_template(self):
        return {'num_q': 1}


class FeedbackOne(Page):

    template_name = 'private_value_auction/Feedback.html'

    def variables_for_template(self):
        return {
            'num_q': 1,
            'is_training_question_1_my_payoff_correct': (
                self.player.is_training_question_1_my_payoff_correct()
            ),
            'answer_you': self.player.training_question_1_my_payoff,
            'correct_answer': Constants.training_question_1_my_payoff_correct
        }


class Bid(Page):

    template_name = 'private_value_auction/Bid.html'

    form_model = models.Player
    form_fields = ['bid_amount']

    def variables_for_template(self):
        if self.player.private_value is None:
            self.player.private_value = self.player.generate_private_value()

        return {'private_value': self.player.private_value,
                'min_bid': Money(Constants.min_allowable_bid),
                'max_bid': Money(Constants.max_allowable_bid)}


class ResultsWaitPage(WaitPage):

    scope = models.Group

    def after_all_players_arrive(self):
        self.group.set_winner()

    def body_text(self):
        return "Waiting for the other participant."


class Results(Page):

    template_name = 'private_value_auction/Results.html'

    def variables_for_template(self):
        if self.player.payoff is None:
            self.player.set_payoff()

        return {'is_winner': self.player.is_winner,
                'bid_amount': self.player.bid_amount,
                'winning_bid': self.group.highest_bid(),
                'second_highest_bid': self.group.second_highest_bid(),
                'private_value': self.player.private_value,
                'payoff': self.player.payoff}


def pages():

    return [Introduction,
            QuestionOne,
            FeedbackOne,
            Bid,
            ResultsWaitPage,
            Results]
