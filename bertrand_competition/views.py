# -*- coding: utf-8 -*-
from __future__ import division
import bertrand_competition.models as models
from bertrand_competition._builtin import Page, WaitPage


class Decide(Page):

    template_name = 'bertrand_competition/Decide.html'

    form_model = models.Player
    form_fields = ['price']

    def variables_for_template(self):
        return {'num_other_players': self.group.players_per_group - 1,
                'marginal_cost': self.subsession.marginal_cost,
                'maximum_price': self.subsession.maximum_price}


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
