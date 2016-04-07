# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):

    def is_displayed(self):
        return  self.subsession.round_number == 1


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.reformed_player()
        self.group.reform()


class ReformApproval(Page):

    form_model = models.Player
    form_fields = ['approval']


class Results(WaitPage):

    def after_all_players_arrive(self):
        self.group.approvals()
        self.group.payoffs()


class FinalResults(Page):

    def is_displayed(self):
        return  self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):

        return {
            'player_payoff': sum([p.payoff for p in self.player.in_all_rounds()]),
            'total_approvals': self.group.approvals(),
            'solidarity': self.group.solidarity_benefits[5]
        }

page_sequence =[
    Introduction,
    ResultsWaitPage,
    ReformApproval,
    Results,
    FinalResults
]
