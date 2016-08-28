# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer
from otree import widgets
from otree.common import Currency as c, currency_range
import random
# </standard imports>
from random import randint

author = 'Dev'

doc = """

In this asset market, two players trade shares that give probabilistic dividends. It is based on
<a href="http://www.tandfonline.com/doi/abs/10.3200/JECE.40.1.027-037">
    Bostian and Holt (2010).
</a>

"""

bibliography = (
    (
        'Smith, Vernon L., Gerry L. Suchanek, and Arlington W. Williams. '
        '"Bubbles, crashes, and endogenous expectations in experimental spot '
        'asset markets."Econometrica: Journal of the Econometric Society '
        '(1988): 1119-1151.'
    ),
    (
        'Smith, Alec, et al. "Irrational exuberance and neural crash warning '
        'signals during endogenous experimental market bubbles." Proceedings '
        'of the National Academy of Sciences 111.29 (2014): 10503-10508.'
    ),
    (
        'Palan, Stefan. "A review of bubbles and crashes in experimental '
        'asset markets." Journal of Economic Surveys 27.3 (2013): 570-588.'
    )
)


class Constants(BaseConstants):
    name_in_url = 'asset_market'
    players_per_group = 2
    num_rounds = 2

    instructions_template = 'asset_market/Instructions.html'

    endowment = c(20)
    num_shares = 10


class Subsession(BaseSubsession):
    def before_session_starts(self):
        if self.round_number == 1:
            for p in self.get_players():
                p.cash = Constants.endowment


class Group(BaseGroup):
    # transaction fields
    transaction_price = models.CurrencyField(doc="""Given by 0.5*(BP+SP)""")
    shares_traded = models.PositiveIntegerField(initial=0)

    # dividend fields
    dividend_per_share = models.CurrencyField()
    is_dividend = models.BooleanField(initial=False,
                                      doc="""Indicates whether dividend is issued""")

    # method to set cash and shares to balance in previous round
    def set_assets_to_previous(self):
        for p in self.get_players():
            p.cash = p.in_previous_rounds()[-1].cash
            p.shares = p.in_previous_rounds()[-1].shares

    def trade(self):
        buyers = [p for p in self.get_players() if p.order_type == 'Buy']
        sellers = [p for p in self.get_players() if p.order_type == 'Sell']
        # both lists must have exactly 1 element
        if not (buyers and sellers):
            return
        buyer = buyers[0]
        seller = sellers[0]
        if seller.sp >= buyer.bp or (buyer.bn * buyer.bp == 0) or (
                seller.sn * seller.sp == 0):
            return

        # average of buy & sell price
        self.transaction_price = 0.5 * (buyer.bp + seller.sp)
        self.shares_traded = min(buyer.bn, seller.sn)

        # adjust shares and cash
        amount = self.transaction_price * self.shares_traded
        if amount > buyer.cash:
            return

        buyer.shares += self.shares_traded
        buyer.cash -= amount

        seller.shares -= self.shares_traded
        seller.cash += amount

    def set_dividend(self):
        self.dividend_per_share = randint(1, 2)
        self.is_dividend = True

        # adjust cash
        for p in self.get_players():
            p.cash += (
                p.shares * self.dividend_per_share
                if p.shares != 0 else
                p.cash
            )


class Player(BasePlayer):
    # initial shares and payoff
    shares = models.PositiveIntegerField(initial=5)

    cash = models.CurrencyField()

    # default allocated shares for both players; provides a range for buyers; sellers' range is limited by the number of shares they have


    # order fields
    bp = models.CurrencyField(initial=0.00,
                              doc="""maximum buying price per share""")
    bn = models.PositiveIntegerField(initial=0,
                                     choices=range(0, Constants.num_shares + 1,
                                                   1),
                                     doc="""number of shares willing to buy""")
    sp = models.CurrencyField(initial=0.00,
                              doc="""minimum selling price per share""")
    sn = models.PositiveIntegerField(initial=0,
                                     doc="""number of shares willing to sell.""")

    order_type = models.CharField(choices=['Sell', 'Buy', 'None'],
                                  doc="""player: buy or sell?""",
                                  widget=widgets.RadioSelectHorizontal)

    def other_player(self):
        """Returns other player in group. Only valid for 2-player groups."""
        return self.get_others_in_group()[0]

    def set_payoff(self):
        self.payoff = 0
        if self.subsession.round_number == Constants.num_rounds:
            self.payoff = self.cash
        else:
            self.payoff = 0
