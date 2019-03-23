from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduction(Page):
    pass


class Request(Page):
    form_model = 'player'
    form_fields = ['request']


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    def vars_for_template(self):
        return {
            'other_player_request': self.player.other_player().request
        }


page_sequence = [
    Introduction,
    Request,
    ResultsWaitPage,
    Results,
]
