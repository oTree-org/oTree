# -*- coding: utf-8 -*-
from __future__ import division
import cournot_competition.models as models
from cournot_competition._builtin import Page, WaitPage


class Decide(Page):

    template_name = 'cournot_competition/Decide.html'

    def variables_for_template(self):
        return {'total_capacity': self.subsession.total_capacity,
                'max_units_per_player': self.subsession.max_units_per_player(),
                'num_other_players': self.group.players_per_group - 1,
                'currency_per_point': self.subsession.currency_per_point}

    form_model = models.Player
    form_fields = ['units']


class ResultsWaitPage(WaitPage):

    scope = models.Group

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):

    template_name = 'cournot_competition/Results.html'

    def variables_for_template(self):

        return {'units': self.player.units,
                'total_units': self.group.total_units,
                'players_per_group': self.group.players_per_group,
                'price_in_points': self.group.price_in_points,
                'payoff_in_points': self.player.payoff_in_points,
                'payoff': self.player.payoff}


def pages():

    return [Decide,
            ResultsWaitPage,
            Results]
