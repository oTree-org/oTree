# -*- coding: utf-8 -*-
import bertrand_competition.forms as forms
from bertrand_competition._builtin import Page, MatchWaitPage, SubsessionWaitPage
from otree.common import Money, money_range


class Introduction(Page):

    template_name = 'bertrand_competition/Introduction.html'

    def variables_for_template(self):
        return {
            'minimum_price': self.treatment.minimum_price,
            'maximum_price': self.treatment.maximum_price
        }


class Compete(Page):

    template_name = 'bertrand_competition/Compete.html'

    def get_form_class(self):
        return forms.PriceForm

class ResultsWaitPage(MatchWaitPage):

    def after_all_players_arrive(self):
        for p in self.match.players:
            p.set_payoff()

class Results(Page):

    template_name = 'bertrand_competition/Results.html'

    def variables_for_template(self):

        return {
            'payoff': self.player.payoff,
            'is_winner': self.player.is_winner,
            'price': self.player.price,
            'other_price': self.player.other_player().price,
            'equal_price': self.player.price == self.player.other_player().price,
        }

def pages():
    return [
        Introduction,
        Compete,
        ResultsWaitPage,
        Results
    ]