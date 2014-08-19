# -*- coding: utf-8 -*-
import prisoner.forms as forms
from prisoner._builtin import Page, MatchWaitPage


class Decision(Page):

    """This page has the instructions and this is where the decision is made.
    Presented to both players in a match at the same time"""

    template_name = 'prisoner/Decision.html'

    def variables_for_template(self):

        return {'friend_amount': self.treatment.friend_amount,
                'betrayed_amount': self.treatment.betrayed_amount,
                'enemy_amount': self.treatment.enemy_amount,
                'betray_amount': self.treatment.betray_amount}

    def get_form_class(self):
        return forms.DecisionForm


class ResultsWaitPage(MatchWaitPage):

    def body_text(self):
        return 'Waiting for the other player to make a decision.'

    def after_all_players_arrive(self):
        for p in self.match.players:
            p.set_payoff()


class Results(Page):

    """Results page to show players the decisions that were made and print the payoffs"""

    template_name = 'prisoner/Results.html'

    def variables_for_template(self):
        return {'my_payoff': self.player.payoff,
                'my_decision': self.player.decision.lower(),
                'other_player_decision': self.player.other_player().decision.lower(),
                'same_choice': self.player.decision == self.player.other_player().decision}


def pages():

    return [Decision,
            ResultsWaitPage,
            Results]
