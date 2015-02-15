# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants

class Introduction(Page):

    template_name = 'common_value_auction/Introduction.html'




class Bid(Page):

    form_model = models.Player
    form_fields = ['bid_amount']

    def vars_for_template(self):
     if  self.player.item_value_estimate is None:
             self.player.item_value_estimate =  self.group.generate_value_estimate()




class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_winner()


class Results(Page):

    def vars_for_template(self):
        if self.player.payoff is None:
            self.player.set_payoff()
        return {
            'is_greedy': self.group.item_value - self.player.bid_amount < 0
        }




page_sequence = [Introduction,
            Bid,
            ResultsWaitPage,
            Results]
