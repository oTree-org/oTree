# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    timeout_seconds = 600
    def is_displayed(self):
        return  self.subsession.round_number == 1

    def vars_for_template(self):
        return {
            'num_others_in_group': Constants.players_per_group - 1,
            'zero': Constants.solidarity_benefits[0],
            'one': Constants.solidarity_benefits[1],
            'two': Constants.solidarity_benefits[2],
            'three': Constants.solidarity_benefits[3],
            'four': Constants.solidarity_benefits[4],
            'five': Constants.solidarity_benefits[5]
        }

class ReformingCalculations(WaitPage):

    def after_all_players_arrive(self):
        self.group.reformed_player()
        # self.group.reform_a_player()


class PreOverthrow(Page):
    timeout_seconds = 120
    def is_displayed(self):
        return self.session.vars['overthrow'] == 0

    def vars_for_template(self):
        if self.subsession.round_number == 1:
            return {
                'reformed_this_round': self.player.participant.vars['reformed_this_round'],
                'current_round': self.subsession.round_number
            }
        else:
            return {
                'total_approvals': self.group.approvals_in_previous_round(),
                'reformed_this_round': self.player.participant.vars['reformed_this_round'],
                'player_payoff_in_previous_round': self.player.in_round(self.subsession.round_number-1).payoff,
                'player_payoff': sum([p.payoff for p in self.player.in_previous_rounds()]),
                'current_round': self.subsession.round_number,
            }

    form_model = models.Player
    form_fields = ['approval','vote_to_overthrow']

class PostOverthrow(Page):
    timeout_seconds = 120
    def is_displayed(self):
        return self.session.vars['overthrow'] == 1

    form_model = models.Player
    form_fields = ['reforms_votes']

    def vars_for_template(self):
        return {
            'player_payoff_in_previous_round': self.player.in_round(self.subsession.round_number-1).payoff,
            'player_payoff': sum([p.payoff for p in self.player.in_previous_rounds()]),
            'overthrow_starts': self.session.vars['overthrow_round'] + 1,
            'current_round': self.subsession.round_number,
            'coordinated_reforms_in_previous_round': self.session.vars['coordinated_reforms']
        }

class PostOverthrowCalculations(WaitPage):

    def is_displayed(self):
        return self.session.vars['overthrow'] == 1

    def after_all_players_arrive(self):
        self.group.reform()
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
        if self.session.vars['overthrow'] == 0:
            return {
                'overthrow': self.session.vars['overthrow'],
                'total_approvals': self.group.approvals(),
                'player_payoff_in_last_round': self.player.payoff,
                'player_payoff': sum([p.payoff for p in self.player.in_all_rounds()])
            }
        else:
            return {
                'overthrow': self.session.vars['overthrow'],
                'player_payoff_in_last_round': self.player.payoff,
                'player_payoff': sum([p.payoff for p in self.player.in_all_rounds()]),
                'current_round': self.subsession.round_number,
                'overthrow_round': self.session.vars['overthrow_round'],
                'coordinated_reforms_in_last_round': self.session.vars['coordinated_reforms']
            }

page_sequence =[
    Introduction,
    ReformingCalculations,
    PreOverthrow,
    PostOverthrow,
    PostOverthrowCalculations,
    PreOverthrowCalculations,
    FinalResults
]
