# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants
from otree.common import safe_json


class Introduction(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1


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

    def vars_for_template(self):
        return {
            'transaction_price': self.group.transaction_price or 0
        }


class DividendWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_dividend()


class Dividend(Page):

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


page_sequence = [
    Introduction,
    OrderWaitPage,
    Order,
    TransactionWaitPage,
    Transaction,
    DividendWaitPage,
    Dividend,
    ResultsWaitPage,
    Results,
]
