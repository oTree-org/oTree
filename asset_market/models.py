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
<p>
In this asset market, two players trade shares that give probabilistic dividends. It is based on
<a href="http://www.tandfonline.com/doi/abs/10.3200/JECE.40.1.027-037">Bostian and Holt (2010).</a><br>
Source code <a href="https://github.com/oTree-org/oTree/tree/master/asset_market" target="_blank">here</a>.
</p>
<h4>Recommended Literature</h4>
<p>
Smith, Vernon L., Gerry L. Suchanek, and Arlington W. Williams. "Bubbles, crashes, and endogenous expectations in experimental spot asset markets."Econometrica: Journal of the Econometric Society (1988): 1119-1151.
Smith, Alec, et al. "Irrational exuberance and neural crash warning signals during endogenous experimental market bubbles." Proceedings of the National Academy of Sciences 111.29 (2014): 10503-10508.
Palan, Stefan. "A review of bubbles and crashes in experimental asset markets." Journal of Economic Surveys 27.3 (2013): 570-588.
</p>
<p>
Wikipedia: <a href="https://en.wikipedia.org/wiki/Stock_market_bubble">Stock Market Bubbles,</a>
<a href="https://en.wikipedia.org/wiki/Experimental_economics#Market_games">Market Games</a><br>
Keywords: Stock Market, Finance, Bubble, Trade,
</p>
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
    dividend_per_share = models.MoneyField(default=1)
    is_dividend = models.BooleanField(default=False, doc="""Indicates whether dividend is issued""")

    def set_payoffs(self):
        for p in self.get_players():
            p.payoff = 0

    def set_transaction(self):
        for p in self.get_players():
            if not self.is_transaction:
                if (p.order_type == 'Buy' and p.other_player().order_type == 'Sell') or (p.order_type == 'Sell' and p.other_player().order_type == 'Buy'):
                    if (p.sp != 0 and p.sn != 0) or (p.bp != 0 and p.bn != 0):
                        if p.bp != 0 and p.other_player().sp <= p.bp:
                            # buyer
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
                        elif p.sp != 0 and p.sp <= p.other_player().bp:
                            # seller
                            # set transaction price
                            self.transaction_price = 0.5*(p.sp+p.other_player().bp)
                            self.shares_traded = min(p.sn, p.other_player().bn)

                            # adjust shares and cash
                            amount = self.transaction_price * self.shares_traded
                            if amount <= p.other_player().cash:
                                # buyer
                                p.other_player().shares += self.shares_traded
                                p.other_player().cash -= self.transaction_price * self.shares_traded
                                # seller
                                p.shares -= self.shares_traded
                                p.cash += self.transaction_price * self.shares_traded
                                self.is_transaction = True

    def set_dividend(self):
        self.dividend_per_share = randint(1,2)
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

    order_type = models.CharField(max_length=10, doc="""determines whether a player wants to buy or sell""", widget=widgets.RadioSelectHorizontal)

    def order_type_choices(self):
        return ['Sell', 'Buy', 'None']

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

    def set_payoff(self):
        self.payoff = 0