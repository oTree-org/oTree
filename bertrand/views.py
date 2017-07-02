from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduction(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1


class Decide(Page):
    form_model = models.Player
    form_fields = ['price']


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    def vars_for_template(self):
        return {
            'table': [
                ('Your price', self.player.price),
                ('Lowest price', min(
                    p.price for p in self.group.get_players())),
                ('Was your product sold?',
                 'Yes' if self.player.is_a_winner else 'No'),
                ('Your profit', self.player.payoff),
            ]
        }


page_sequence = [Introduction,
                 Decide,
                 ResultsWaitPage,
                 Results]
