# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants
from otree.common import safe_json


def vars_for_all_templates(self):
    return {
        'total_q': 2,
        'round_num': self.subsession.round_number,
        'num_of_rounds': Constants.num_rounds,  # no of periods
        'num_participants': Constants.players_per_group,
    }


class Introduction(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1


class Instructions(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1


class Question1(Page):

    form_model = models.Player
    form_fields = ['understanding_question_1']

    template_name = 'asset_market/Question.html'

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {
            'num_q': 1,
        }


class Feedback1(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

    template_name = 'asset_market/Feedback.html'

    def vars_for_template(self):
        return {
            'num_q': 1,
            'answer': self.player.understanding_question_1,
            'correct': Constants.understanding_1_correct,
            'is_correct': self.player.is_understanding_question_1_correct(),
        }


class Question2(Page):

    form_model = models.Player
    form_fields = ['understanding_question_2']

    def is_displayed(self):
        return self.subsession.round_number == 1

    template_name = 'asset_market/Question.html'

    def vars_for_template(self):
        return {
            'num_q': 2,
        }


class Feedback2(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

    template_name = 'asset_market/Feedback.html'



    def vars_for_template(self):
        return {
            'num_q': 2,
            'answer': self.player.understanding_question_2,
            'correct': Constants.understanding_2_correct,
            'is_correct': self.player.is_understanding_question_2_correct(),
        }


class OrderWaitPage(WaitPage):

    def after_all_players_arrive(self):
        if self.subsession.round_number > 1:
            self.group.set_assets_to_previous()


class Order(Page):

    form_model = models.Player
    form_fields = ['order_type', 'bp', 'bn', 'sn', 'sp']

    def sn_choices(self):
        return range(0, self.player.shares + 1, 1)

    def bp_choices(self):
        return currency_range(0, self.player.cash, 0.5)

    def sp_choices(self):
        return currency_range(0, self.player.cash, 0.5)



class TransactionWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.trade()


class Transaction(Page):

    def is_displayed(self):
        return True

    def vars_for_template(self):
        return {
            'transaction_price': self.group.transaction_price or 0
        }

class DividendWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_dividend()


class Dividend(Page):

    def is_displayed(self):
        return True

    def vars_for_template(self):
        return {
            'dividend_gain': self.group.dividend_per_share * self.player.shares if self.player.shares != 0 else 0
        }


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_payoff()


class Results(Page):

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def total_payoff(self):
        return self.player.payoff + self.player.participant.session.participation_fee

    def vars_for_template(self):

        # create chart lists
        transaction_price_list = []
        dividend_per_share_list = []
        shares_traded_list = []

        for p in self.player.in_all_rounds():
            transaction_price_list.append(int(p.group.transaction_price or 0))
            dividend_per_share_list.append(int(p.group.dividend_per_share))
            shares_traded_list.append(p.group.shares_traded)

        return {

            'transaction_price_list': safe_json(transaction_price_list),
            'dividend_per_share_list': safe_json(dividend_per_share_list),
            'shares_traded_list': safe_json(shares_traded_list),
        }


page_sequence=[
         Introduction,
         Instructions,
         Question1,
         Feedback1,
         Question2,
         Feedback2,
        OrderWaitPage,
        Order,
        TransactionWaitPage,
        Transaction,
        DividendWaitPage,
        Dividend,
        ResultsWaitPage,
        Results,
    ]
