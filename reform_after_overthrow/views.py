# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):

    def is_displayed(self):
        return  self.subsession.round_number == 3333


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.reformed_player()
        self.group.reform()


class Decisions(Page):

    form_model = models.Player
    form_fields = ['reforms_vote']


class Results(WaitPage):

    def after_all_players_arrive(self):
        self.group.approvals()
        self.group.payoffs()


class FinalResults(Page):

    def is_displayed(self):
        return  self.subsession.round_number == Constants.num_rounds or self.group.abolish() >= Constants.points_to_abolish

    def vars_for_template(self):

        return {
            'player_payoff': sum([p.participant.vars['payoff'] for p in self.player.in_all_rounds()]),
            'total_approvals': self.group.approvals(),
            'solidarity': self.group.solidarity_benefits[5]
        }

page_sequence =[
    Introduction,
    ResultsWaitPage,
    Decisions,
    Results,
    FinalResults
]
