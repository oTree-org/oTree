# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants

class Decision(Page):

    form_model = models.Player
    form_fields = ['decision']


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_payoff()

    body_text = "Waiting for the other player."


class Results(Page):

    def vars_for_template(self):
        return {
            'same_choice': self.player.decision == self.player.other_player().decision
        }


page_sequence = [Decision,
            ResultsWaitPage,
            Results]
