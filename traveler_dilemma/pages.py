from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduction(Page):
    pass


class Claim(Page):

    form_model = 'player'
    form_fields = ['claim']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    def vars_for_template(self):
        return dict(other_player_claim=self.player.other_player().claim)


page_sequence = [Introduction, Claim, ResultsWaitPage, Results]
