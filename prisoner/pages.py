from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduction(Page):
    timeout_seconds = 100


class Decision(Page):
    form_model = 'player'
    form_fields = ['decision']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    def vars_for_template(self):
        me = self.player
        opponent = me.other_player()
        return dict(
            my_decision=me.get_decision_display(),
            opponent_decision=opponent.get_decision_display(),
            same_choice=me.get_decision_display() == opponent.get_decision_display(),
        )


page_sequence = [Introduction, Decision, ResultsWaitPage, Results]
