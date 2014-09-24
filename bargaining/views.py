# -*- coding: utf-8 -*-
import bargaining.models as models
from bargaining._builtin import Page, MatchWaitPage, SubsessionWaitPage
from otree.common import Money, money_range


class Introduction(Page):

    template_name = 'bargaining/Introduction.html'

    def variables_for_template(self):
        return {
            'amount_shared': self.treatment.amount_shared,
        }


class Request(Page):

    template_name = 'bargaining/Request.html'

    form_model = models.Player
    form_fields = ['request_amount']

    def variables_for_template(self):
        return {
            'amount_shared': self.treatment.amount_shared,
        }


class ResultsWaitPage(MatchWaitPage):

    def after_all_players_arrive(self):
        self.match.set_payoffs()


class Results(Page):

    template_name = 'bargaining/Results.html'

    def variables_for_template(self):
        return {
            'payoff': self.player.payoff,
            'request_amount': self.player.request_amount,
            'other_request': self.player.other_player().request_amount
        }


def pages():
    return [
        Introduction,
        Request,
        ResultsWaitPage,
        Results
    ]