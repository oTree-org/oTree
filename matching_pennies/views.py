# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants


class Introduction(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1


class Choice(Page):
    form_model = models.Player
    form_fields = ['penny_side']


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()

    body_text = "Waiting for your opponent."


class Results(Page):
    pass


class ResultsSummary(Page):
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):
        player_in_all_rounds = self.player.in_all_rounds()
        total_payoff = sum([p.payoff for p in player_in_all_rounds])

        return {'player_in_all_rounds': player_in_all_rounds,
                'total_payoff': total_payoff}


page_sequence = [Introduction,
                 Choice,
                 ResultsWaitPage,
                 Results,
                 ResultsSummary]
