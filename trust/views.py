# -*- coding: utf-8 -*-
import trust.models as models
from trust._builtin import Page, MatchWaitPage


class Introduction(Page):

    template_name = 'trust/Introduction.html'

    def variables_for_template(self):
        return {'amount_allocated': self.treatment.amount_allocated}


class Send(Page):

    """This page is only for P1
    P1 sends amount (all, some, or none) to P2
    This amount is tripled by experimenter, i.e if sent amount by P1 is 0.50, amount received by P2 is 1.50"""

    template_name = 'trust/Send.html'

    form_model = models.Match
    form_fields = ['sent_amount']

    def participate_condition(self):
        return self.player.index_among_players_in_match == 1

    def variables_for_template(self):
        return {'amount_allocated': self.treatment.amount_allocated}


class SimpleWaitPage(MatchWaitPage):

    def body_text(self):
        return 'The other player has been given the opportunity to give money first. Please wait.'


class SendBack(Page):

    """This page is only for P2
    P2 sends back some amount (of the tripled amount received) to P1"""

    template_name = 'trust/SendBack.html'

    form_model = models.Match
    form_fields = ['sent_back_amount']

    def participate_condition(self):
        return self.player.index_among_players_in_match == 2

    def variables_for_template(self):
        tripled_amount = self.match.sent_amount * 3
        total_amount = self.treatment.amount_allocated + tripled_amount

        return {'amount_allocated': self.treatment.amount_allocated,
                'sent_amount': self.match.sent_amount,
                'tripled_amount': tripled_amount,
                'total_amount': total_amount}


class ResultsWaitPage(MatchWaitPage):

    def body_text(self):
        return 'Waiting for the other player to finish.'

    def after_all_players_arrive(self):
        self.match.set_payoffs()


class Results(Page):

    """This page displays the earnings of each player"""

    template_name = 'trust/Results.html'

    def variables_for_template(self):

        player1_payoff = self.match.get_player_by_index(1).payoff
        player2_payoff = self.match.get_player_by_index(2).payoff

        tripled_amount = self.match.sent_amount * 3

        return {'amount_allocated': self.treatment.amount_allocated,
                'sent_amount': self.match.sent_amount,
                'tripled_amount': tripled_amount,
                'sent_back_amount': self.match.sent_back_amount,
                'player_index': self.player.index_among_players_in_match,
                'player1_payoff': player1_payoff,
                'player2_payoff': player2_payoff}


def pages():

    return [Introduction,
            Send,
            SimpleWaitPage,
            SendBack,
            ResultsWaitPage,
            Results]
