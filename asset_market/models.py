# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
from otree import widgets
from otree.common import Money, money_range
import random
# </standard imports>


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

    def set_payoffs(self):
        for p in self.get_players():
            p.payoff = 0  # TODO modify this

    def set_transaction(self):
        for p in self.get_players():
            if p.order_type != None and p.order_type != p.other_player().order_type and (p.bp != 0 or p.sp != 0) :
                if p.order_type == "Buy Order" and (p.bp >= p.other_player().sp):
                    self.transaction_price = 0.5*(p.bp+p.other_player().sp)
                    self.shares_traded = min(p.bn, p.other_player().sn)
                    self.is_transaction = True
                    # TODO reduce shares and amount



class Player(otree.models.BasePlayer):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    group = models.ForeignKey(Group, null = True)
    # </built-in>

    # initial shares and cash
    cash = models.MoneyField(default=20)
    shares = models.PositiveIntegerField(default=5)

    # order fields
    order_type = models.CharField(max_length=10, choices=['Buy Order', 'Sell Order', 'None'], widget=widgets.RadioSelect())
    bp = models.MoneyField(default=0.00, doc="""maximum buying price per share""")
    bn = models.PositiveIntegerField(default=0, doc="""number of shares willing to buy""")
    sp = models.MoneyField(default=0.00, doc="""minimum selling price per share""")
    sn = models.PositiveIntegerField(default=0, doc="""number of shares willing to sell.""")

    def other_player(self):
        """Returns other player in group. Only valid for 2-player groupes."""
        return self.get_others_in_group()[0]

    QUESTION_1_CHOICES = ['P=3, N=2','P=2, N=3','P=2.5, N=3','P=2.5, N=2','No transaction will take place',]
    QUESTION_2_CHOICES = ['$8, $12', '$12, $8', '$8, $8', '$12, $12', '$10, $10']

    understanding_question_1 = models.CharField(max_length=100, null=True, choices=QUESTION_1_CHOICES, verbose_name='', widget=widgets.RadioSelect())
    understanding_question_2 = models.CharField(max_length=100, null=True, choices=QUESTION_2_CHOICES, verbose_name='', widget=widgets.RadioSelect())

    # check correct answers
    def is_understanding_question_1_correct(self):
        return self.understanding_question_1 == self.subsession.understanding_1_correct

    def is_understanding_question_2_correct(self):
        return self.understanding_question_2 == self.subsession.understanding_2_correct


    def my_field_error_message(self, value):
        if not 0 <= value <= 10:
            return 'Value is not in allowed range'


    def role(self):
        # you can make this depend of self.id_in_group
        return ''

