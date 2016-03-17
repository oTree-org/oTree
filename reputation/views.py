# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Send(Page):

    form_model = models.Group
    form_fields = ['sent']

    def is_displayed(self):
        return self.player.id_in_group == 1

    def vars_for_template(self):
        return { 'uncooperative': self.group.is_uncooperative() }

class SendBack(Page):
    form_model = models.Group
    form_fields = ['sent_back']

    def is_displayed(self):
        return self.player.id_in_group == 2

    def vars_for_template(self):
        return {
            'multiplied': self.group.multiplication(),
            'uncooperative': self.group.is_uncooperative()
        }

    def sent_back_error_message(self, value):
        if not (value >= 0 and value <= self.group.multiplication()):
            return 'You don\'t have this kind of money!'

class Bribe(Page):
    form_model = models.Group
    form_fields = ['bribe']

    # determination whether receiver is eligible to pay bribe
    def is_displayed(self):
        return self.player.id_in_group == 2 and random.random() > 0.0000001 and (self.group.fine() > 0)

    def vars_for_template(self):
        return {
            'max_bribe': self.group.fine()*6,
            'fine': self.group.fine()
        }

    def bribe_error_message(self, value):
        if not (value >= 0 and value <= self.group.fine()*6):
            return 'Please enter number between 0 and your maximum bribe'

class WaitForP1(WaitPage):
    pass

class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()

class FinalResults(Page):

    def is_displayed(self):
        return  self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):

        return {
            'player_payoff': sum([p.payoff for p in self.player.in_all_rounds()])
        }


page_sequence = [
    Send,
    WaitForP1,
    SendBack,
    Bribe,
    ResultsWaitPage,
    FinalResults,
]