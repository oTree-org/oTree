from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    pass


class Decision(Page):
    form_model = 'player'
    form_fields = ['volunteer']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    pass


page_sequence = [Introduction, Decision, ResultsWaitPage, Results]
