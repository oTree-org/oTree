from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        group = self.group
        players = group.get_players()
        contributions = [p.contribution for p in players]
        group.total_contribution = sum(contributions)
        group.individual_share = group.total_contribution * Constants.multiplier / Constants.players_per_group
        for p in players:
            p.payoff = Constants.endowment - p.contribution + group.individual_share



class Results(Page):
    pass


page_sequence = [
    Contribute,
    ResultsWaitPage,
    Results
]
