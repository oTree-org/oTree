# -*- coding: utf-8 -*-
from __future__ import division
"""Documentation at https://github.com/oTree-org/otree/wiki"""

from otree.db import models
import otree.models
from otree.common import Money, money_range
from otree import forms


author = 'Your name here'

doc = """
In this asset market, there are 2 participants. Both of you are endowed with $20 cash and 5 shares of stock.
Shares pay random dividends at the end of each period. There are 5 periods during which you are free to submit buy/sell orders to trade
shares. At the end of the study, your cash positions count for your payoffs; your shares are redeemed for free.<br>
Source code <a href="https://github.com/oTree-org/oTree/tree/master/asset_market" target="_blank">here</a>.

"""

class Subsession(otree.models.BaseSubsession):

    name_in_url = 'asset_market'


class Treatment(otree.models.BaseTreatment):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>


    understanding_1_correct = 'P=2.5, N=2'
    understanding_2_correct = '$8, $12'


class Match(otree.models.BaseMatch):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    treatment = models.ForeignKey(Treatment)
    # </built-in>

    players_per_match = 1

    def set_payoffs(self):
        for p in self.players:
            p.payoff = 0 # change to whatever the payoff should be


class Player(otree.models.BasePlayer):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    treatment = models.ForeignKey(Treatment, null = True)
    match = models.ForeignKey(Match, null = True)
    # </built-in>

    def other_player(self):
        """Returns other player in match. Only valid for 2-player matches."""
        return self.other_players_in_match()[0]

    QUESTION_1_CHOICES = ['P=3, N=2','P=2, N=3','P=2.5, N=3','P=2.5, N=2','No transaction will take place',]
    QUESTION_2_CHOICES = ['$8, $12', '$12, $8', '$8, $8', '$12, $12', '$10, $10']

    understanding_question_1 = models.CharField(max_length=100, null=True, choices=QUESTION_1_CHOICES, verbose_name='', widget=forms.RadioSelect())
    understanding_question_2 = models.CharField(max_length=100, null=True, choices=QUESTION_2_CHOICES, verbose_name='', widget=forms.RadioSelect())

    # check correct answers
    def is_understanding_question_1_correct(self):
        return self.understanding_question_1 == self.treatment.understanding_1_correct

    def is_understanding_question_2_correct(self):
        return self.understanding_question_2 == self.treatment.understanding_2_correct


    def my_field_error_message(self, value):
        if not 0 <= value <= 10:
            return 'Value is not in allowed range'


    def role(self):
        # you can make this depend of self.index_among_players_in_match
        return ''

def treatments():
    return [Treatment.create()]