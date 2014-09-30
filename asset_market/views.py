# -*- coding: utf-8 -*-
from __future__ import division
import otree.views
import asset_market.models as models
from asset_market._builtin import Page, WaitPage
from otree.common import Money, money_range

def variables_for_all_templates(self):
    return {
        'total_q': 2,
        'round_num': self.subsession.round_number,
        'num_of_rounds': self.subsession.number_of_rounds,  # no of periods
        'num_participants': self.match.players_per_match,
        'cash': self.player.cash,
        'shares': self.player.shares,
    }

class Introduction(Page):

    def participate_condition(self):
        return self.subsession.round_number == 1

    template_name = 'asset_market/Introduction.html'


class Instructions(Page):

    def participate_condition(self):
        return self.subsession.round_number == 1

    template_name = 'asset_market/Instructions.html'


class QuestionOne(Page):

    form_model = models.Player
    form_fields = ['understanding_question_1']

    def participate_condition(self):
        return self.subsession.round_number == 1

    template_name = 'asset_market/Question.html'

    def variables_for_template(self):
        return {
            'num_q': 1,
        }

class FeedbackOne(Page):

    def participate_condition(self):
        return self.subsession.round_number == 1

    template_name = 'asset_market/Feedback.html'

    def variables_for_template(self):
        return {
            'num_q': 1,
            'answer': self.player.understanding_question_1,
            'correct': self.treatment.understanding_1_correct,
            'is_correct': self.player.is_understanding_question_1_correct(),
        }

class QuestionTwo(Page):

    form_model = models.Player
    form_fields = ['understanding_question_2']

    def participate_condition(self):
        return self.subsession.round_number == 1

    template_name = 'asset_market/Question.html'

    def variables_for_template(self):
        return {
            'num_q': 2,
        }

class FeedbackTwo(Page):

    def participate_condition(self):
        return self.subsession.round_number == 1

    template_name = 'asset_market/Feedback.html'

    def variables_for_template(self):
        return {
            'num_q': 2,
            'answer': self.player.understanding_question_2,
            'correct': self.treatment.understanding_2_correct,
            'is_correct': self.player.is_understanding_question_2_correct(),
        }


class Order(Page):

    def participate_condition(self):
        return True

    form_model = models.Player
    form_fields = ['order_type', 'bp', 'bn', 'sp', 'sn']

    template_name = 'asset_market/Order.html'

    def variables_for_template(self):
        return {
            'cash': self.player.cash,
            'shares': self.player.shares,
        }


class TransactionWaitPage(WaitPage):

    group = models.Match

    def after_all_players_arrive(self):
        self.match.set_transaction()

class Transaction(Page):

    def participate_condition(self):
        return True

    template_name = 'asset_market/Transaction.html'

    def variables_for_template(self):
        return {
            'cash': self.player.cash,
            'shares': self.player.shares,
            'transaction': self.match.is_transaction,
        }


class Dividend(Page):

    def participate_condition(self):
        return True

    template_name = 'asset_market/Dividend.html'

    def variables_for_template(self):
        return {
            'cash': self.player.cash,
            'shares': self.player.shares,
        }

class ResultsWaitPage(WaitPage):

    group = models.Match

    def after_all_players_arrive(self):
        self.match.set_payoffs()

class Results(Page):

    def participate_condition(self):
        return self.subsession.round_number == self.subsession.number_of_rounds

    template_name = 'asset_market/Results.html'

def pages():
    return [
        Introduction,
        Instructions,
        QuestionOne,
        FeedbackOne,
        QuestionTwo,
        FeedbackTwo,
        Order,
        TransactionWaitPage,
        Transaction,
        Dividend,
        ResultsWaitPage,
        Results
    ]