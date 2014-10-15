# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
from otree import widgets
from otree.common import Money, money_range
import random
# </standard imports>
from random import randint


author = 'Dev'

doc = """
In this asset market, there are 2 participants. Both of you are endowed with $20 cash and 5 shares of stock.
Shares pay random dividends at the end of each period. There are 5 periods during which you are free to submit buy/sell orders to trade
shares. At the end of the study, your cash positions count for your payoffs; your shares are redeemed for free.<br>
Source code <a href="https://github.com/oTree-org/oTree/tree/master/asset_market" target="_blank">here</a>.
"""

class Constants:
    understanding_1_correct = 'P=2.5, N=2'
    understanding_2_correct = '$8, $12'


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'asset_market'



class Group(otree.models.BaseGroup):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_group = 2

    # transaction fields
    is_transaction = models.BooleanField(default=False, doc="""Indicates whether there is a transaction""")
    transaction_price = models.MoneyField(null=True, doc="""Given by 0.5*(BP+SP)""")
    shares_traded = models.PositiveIntegerField(null=True)

    # dividend fields
    dividend_per_share = models.MoneyField(null=True)
    is_dividend = models.BooleanField(default=False, doc="""Indicates whether dividend is issued""")

    def set_payoffs(self):
        for p in self.get_players():
            p.payoff = 0

    def set_transaction(self):
        for p in self.get_players():
            if (p.sp != 0 and p.sn != 0) or (p.bp != 0 and p.bn != 0):
                # FIXME consider the following conditions.
                '''
                 -A transaction is only possible when one participant wants to buy and the other to sell.
                 -Moreover, the submitted maximum buying price (BP) has to be higher than the minimum selling price (SP).
                 -When this is the case, transaction takes place at the average of these two prices.
                  That is transaction price (P) = 0.5*(BP+SP).
                 -The number of shares traded (N) equals the smaller of the two numbers, i.e. N is the minimum of BN and SN.
                 -If transaction takes place, N shares are removed from the selling party to the buying party; accordingly,
                 cash equal to the transaction price (P) is added to the selling party and subtracted from the buying party.
                 -Otherwise, no transaction takes place and the orders submitted, if any, are not revealed to participants.
                '''

                # set transaction price
                self.transaction_price = 0.5*(p.bp+p.other_player().sp)
                self.shares_traded = min(p.bn, p.other_player().sn)

                # adjust shares and cash
                amount = self.transaction_price * self.shares_traded
                if amount <= p.cash:
                    # buyer
                    p.shares += self.shares_traded
                    p.cash -= self.transaction_price * self.shares_traded
                    # seller
                    p.other_player().shares -= self.shares_traded
                    p.other_player().cash += self.transaction_price * self.shares_traded
                    self.is_transaction = True
            else:
                # no transaction
                pass

    def set_dividend(self):
        for p in self.get_players():
            # set dividend - a random value 1 or 2
            self.dividend_per_share = randint(1,2)

            # add dividend to current cash position
            p.cash += (p.shares * self.dividend_per_share)

            self.is_dividend = True


class Player(otree.models.BasePlayer):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    group = models.ForeignKey(Group, null = True)
    # </built-in>

    # initial shares and cash
    cash = models.MoneyField(default=20)
    shares = models.PositiveIntegerField(default=5)

    # order fields
    bp = models.MoneyField(default=0.00, doc="""maximum buying price per share""")
    bn = models.PositiveIntegerField(default=0, doc="""number of shares willing to buy""")
    sp = models.MoneyField(default=0.00, doc="""minimum selling price per share""")
    sn = models.PositiveIntegerField(default=0, doc="""number of shares willing to sell.""")

    def bn_choices(self):
        return range(0, self.shares+1, 1)

    def bn_error_message(self, value):
        pass

    def sn_choices(self):
        return range(0, self.shares+1, 1)

    def bp_choices(self):
        return money_range(0, self.cash, 0.5)

    def sp_choices(self):
        return money_range(0, self.cash, 0.5)

    def other_player(self):
        """Returns other player in group. Only valid for 2-player groups."""
        return self.get_others_in_group()[0]

    QUESTION_1_CHOICES = ['P=3, N=2','P=2, N=3','P=2.5, N=3','P=2.5, N=2','No transaction will take place',]
    QUESTION_2_CHOICES = ['$8, $12', '$12, $8', '$8, $8', '$12, $12', '$10, $10']

    understanding_question_1 = models.CharField(max_length=100, null=True, choices=QUESTION_1_CHOICES, verbose_name='', widget=widgets.RadioSelect())
    understanding_question_2 = models.CharField(max_length=100, null=True, choices=QUESTION_2_CHOICES, verbose_name='', widget=widgets.RadioSelect())

    feedbackq = models.CharField(null=True, verbose_name='How well do you think this sample game was implemented?', widget=widgets.RadioSelectHorizontal())

    def feedbackq_choices(self):
        return ['Very well', 'Well', 'OK', 'Badly', 'Very badly']

    # check correct answers
    def is_understanding_question_1_correct(self):
        return self.understanding_question_1 == Constants.understanding_1_correct

    def is_understanding_question_2_correct(self):
        return self.understanding_question_2 == Constants.understanding_2_correct