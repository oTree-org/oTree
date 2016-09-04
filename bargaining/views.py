from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduction(Page):
    pass


class Request(Page):
    form_model = models.Player
    form_fields = ['request_amount']


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    def vars_for_template(self):
        return {
            'sum': self.player.request_amount + self.player.other_player().request_amount,
            'earn': self.player.payoff
        }


page_sequence = [
    Introduction,
    Request,
    ResultsWaitPage,
    Results,
]
