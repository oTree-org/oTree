from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduction(Page):
    def before_next_page(self):
        self.player.item_value_estimate = self.group.generate_value_estimate()


class Bid(Page):
    form_model = models.Player
    form_fields = ['bid_amount']


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_winner()
        for p in self.group.get_players():
            p.set_payoff()


class Results(Page):
    def vars_for_template(self):
        return {
            'is_greedy': self.group.item_value - self.player.bid_amount < 0
        }


page_sequence = [Introduction,
                 Bid,
                 ResultsWaitPage,
                 Results]
