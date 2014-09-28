# -*- coding: utf-8 -*-
import cournot_competition.models as models
from cournot_competition._builtin import Page, WaitPage


class Decide(Page):

    template_name = 'cournot_competition/Decide.html'

    def variables_for_template(self):
        return {'total_capacity': self.treatment.total_capacity,
                'max_units_per_player': self.treatment.max_units_per_player(),
                'num_other_players': self.match.players_per_match - 1,
                'currency_per_point': self.treatment.currency_per_point}

    form_model = models.Player
    form_fields = ['units']


class ResultsWaitPage(WaitPage):

    group = models.Match

    def after_all_players_arrive(self):
        self.match.set_payoffs()


class Results(Page):

    template_name = 'cournot_competition/Results.html'

    def variables_for_template(self):

        return {'units': self.player.units,
                'total_units': self.match.total_units,
                'players_per_match': self.match.players_per_match,
                'price_in_points': self.match.price_in_points,
                'payoff_in_points': self.player.payoff_in_points,
                'payoff': self.player.payoff}


def pages():

    return [Decide,
            ResultsWaitPage,
            Results]
