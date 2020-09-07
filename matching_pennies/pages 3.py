from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Choice(Page):
    form_model = 'player'
    form_fields = ['penny_side']

    def vars_for_template(self):
        return dict(player_in_previous_rounds=self.player.in_previous_rounds())


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class ResultsSummary(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        player_in_all_rounds = self.player.in_all_rounds()

        return dict(
            total_payoff=sum([p.payoff for p in player_in_all_rounds]),
            paying_round=self.session.vars['paying_round'],
            player_in_all_rounds=player_in_all_rounds,
        )


page_sequence = [Choice, ResultsWaitPage, ResultsSummary]
