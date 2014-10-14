# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Money, money_range
from .models import Constants

class Decide(Page):

    template_name = 'bertrand_competition/Decide.html'

    form_model = models.Player
    form_fields = ['price']

    def variables_for_template(self):
        return {'num_other_players': self.group.players_per_group - 1,
                'marginal_cost': Constants.marginal_cost,
                'maximum_price': Constants.maximum_price}


class ResultsWaitPage(WaitPage):

    scope = models.Group

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):

    template_name = 'bertrand_competition/Results.html'

    def variables_for_template(self):

        return {'is_sole_winner': self.player.is_sole_winner(),
                'is_shared_winner': self.player.is_shared_winner(),
                'price': self.player.price,
                'payoff': self.player.payoff,
                'num_winners': self.group.num_winners,
                'winning_price': self.group.winning_price}


def pages():

    return [Decide,
            ResultsWaitPage,
            Results]
