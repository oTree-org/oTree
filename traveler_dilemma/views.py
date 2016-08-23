# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants



class Introduction(Page):
    pass


class Claim(Page):

    form_model = models.Player
    form_fields = ['claim']


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_payoff()


class Results(Page):

    def vars_for_template(self):
        other = self.player.other_player().claim
        if self.player.claim < other:
            reward = Constants.reward
            penalty = c(0)
        elif self.player.claim > other:
            reward = c(0)
            penalty = Constants.penalty
        else:
            reward = c(0)
            penalty = c(0)
        return {
            'reward': reward,
            'penalty': penalty,
            'amount_paid_to_both': self.player.payoff - reward,
        }


page_sequence = [
    Introduction,
    Claim,
    ResultsWaitPage,
    Results
]
