# -*- coding: utf-8 -*-
import bertrand_competition.forms as forms
from bertrand_competition._builtin import Page, MatchWaitPage, SubsessionWaitPage
from otree.common import Money, money_range

class Decide(Page):

    template_name = 'bertrand_competition/Decide.html'

    def get_form_class(self):
        return forms.PriceForm

    def variables_for_template(self):
        return {
            'marginal_cost': self.treatment.marginal_cost,
            'maximum_price': self.treatment.maximum_price
        }


class ResultsWaitPage(MatchWaitPage):

    def after_all_players_arrive(self):
        self.match.set_payoffs()

class Results(Page):

    template_name = 'bertrand_competition/Results.html'

    def variables_for_template(self):

        return {
            'is_sole_winner': self.player.is_sole_winner(),
            'is_shared_winner': self.player.is_shared_winner(),
            'price': self.player.price,
            'payoff': self.player.payoff,
            'num_winners': self.match.num_winners,
            'winning_price': self.match.winning_price,
        }

def pages():
    return [
        Decide,
        ResultsWaitPage,
        Results
    ]