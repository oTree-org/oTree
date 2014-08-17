# -*- coding: utf-8 -*-
import stackelberg_competition.forms as forms
from stackelberg_competition.utilities import Page, MatchWaitPage, SubsessionWaitPage
from otree.common import Money, money_range


class Introduction(Page):

    template_name = 'stackelberg_competition/Introduction.html'

    def variables_for_template(self):
        return {
            'total_capacity': self.treatment.total_capacity
        }


class ChoiceOne(Page):

    def participate_condition(self):
        return self.player.index_among_players_in_match == 1

    template_name = 'stackelberg_competition/ChoiceOne.html'

    def get_form_class(self):
        return forms.QuantityForm


class ChoiceTwo(Page):

    def participate_condition(self):
        return self.player.index_among_players_in_match == 2

    template_name = 'stackelberg_competition/ChoiceTwo.html'

    def get_form_class(self):
        return forms.QuantityForm

    def variables_for_template(self):
        return {
            'other_quantity': self.player.other_player().quantity
        }

class ResultsWaitPage(MatchWaitPage):
    def after_all_players_arrive(self):
        for p in self.match.players:
            p.set_payoff()

class Results(Page):

    template_name = 'stackelberg_competition/Results.html'

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
        ChoiceOne,
        MatchWaitPage,
        ChoiceTwo,
        ResultsWaitPage,
        Results
    ]