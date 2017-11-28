from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduction(Page):
    timeout_seconds = 100


class Decision(Page):
    form_model = models.Player
    form_fields = ['cooperate']


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_payoff()


class Results(Page):
    def vars_for_template(self):
        opponent = self.player.other_player()
        return {
            'my_decision': self.player.decision_label(),
            'other_player_decision': opponent.decision_label(),
            'same_choice': self.player.cooperate == opponent.cooperate,
        }


page_sequence = [
    Introduction,
    Decision,
    ResultsWaitPage,
    Results
]
