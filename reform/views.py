# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):

    def is_displayed(self):
        return  self.subsession.round_number == 333


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.reformed_player()
        self.group.reform_a_player()


class PreOverthrow(Page):

    def is_displayed(self):
        return self.session.vars['overthrow'] == 0

    form_model = models.Player
    form_fields = ['approval','vote_to_overthrow']

class PostOverthrow(Page):

    def is_displayed(self):
        return self.session.vars['overthrow'] == 1

    form_model = models.Player
    form_fields = ['reforms_votes']

class PostOverthrowCalculations(WaitPage):

    def is_displayed(self):
        return self.session.vars['overthrow'] == 1

    def after_all_players_arrive(self):
        self.group.payoffs()

class PreOverthrowCalculations(WaitPage):

    def is_displayed(self):
        return self.session.vars['overthrow'] == 0

    def after_all_players_arrive(self):
        self.group.approvals()
        self.group.payoffs()
        self.group.total_votes_for_overthrow()


class FinalResults(Page):

    def is_displayed(self):
        return  self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):

        return {
            'player_payoff': sum([p.payoff for p in self.player.in_all_rounds()])
        }

page_sequence =[
    Introduction,
    ResultsWaitPage,
    PreOverthrow,
    PostOverthrow,
    PostOverthrowCalculations,
    PreOverthrowCalculations,
    FinalResults
]
