# -*- coding: utf-8 -*-
import cournot_competition.forms as forms
from cournot_competition.utilities import Page, MatchWaitPage, SubsessionWaitPage
from otree.common import Money, money_range


class Introduction(Page):
    template_name = 'cournot_competition/Introduction.html'

    def variables_for_template(self):
        return {
            'total_capacity': self.treatment.total_capacity
        }


class Compete(Page):
    template_name = 'cournot_competition/Compete.html'

    def get_form_class(self):
        return forms.QuantityForm

class ResultsWaitPage(MatchWaitPage):

    def action(self):
        for p in self.match.players:
            p.set_payoff()

class Results(Page):


    template_name = 'cournot_competition/Results.html'

    def variables_for_template(self):

        return {
            'payoff': self.player.payoff,
            'quantity': self.player.quantity,
            'other_quantity': self.player.other_player().quantity,
            'price': self.match.price
        }


def pages():
    return [
        Introduction,
        Compete,
        ResultsWaitPage,
        Results
    ]