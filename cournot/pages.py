from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduction(Page):
    pass


class Decide(Page):
    form_model = 'player'
    form_fields = ['units']


class ResultsWaitPage(WaitPage):
    body_text = "Waiting for the other participant to decide."

    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    def vars_for_template(self):
        return dict(other_player_units=self.player.other_player().units)


page_sequence = [Introduction, Decide, ResultsWaitPage, Results]
