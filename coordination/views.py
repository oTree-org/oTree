# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Money, money_range


class Choice(Page):

    def participate_condition(self):
        return True

    template_name = 'coordination/Choice.html'

    form_model = models.Player
    form_fields = ['choice']

    def variables_for_template(self):
        return {'group_amount': self.subsession.group_amount,
                'mismatch_amount': self.subsession.mismatch_amount}


class ResultsWaitPage(WaitPage):

    scope = models.Group

    def after_all_players_arrive(self):
        self.group.set_payoffs()

    def body_text(self):
        return "Waiting for the other player."


class Results(Page):


    def participate_condition(self):
        return True

    template_name = 'coordination/Results.html'

    def variables_for_template(self):
        return {'payoff': self.player.payoff,
                'choice': self.player.choice,
                'other_choice': self.player.other_player().choice,
                'same_choice': self.player.choice == self.player.other_player().choice}


def pages():

    return [Choice,
            ResultsWaitPage,
            Results]
