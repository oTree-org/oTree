# -*- coding: utf-8 -*-
import prisoner.forms as forms
from prisoner.utilities import Page, MatchWaitPage


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

    def action(self):
        for p in self.match.participants():
            p.set_payoff()


class Results(Page):

    """Results page to show players the decisions that were made and print the payoffs"""

    template_name = 'prisoner/Results.html'

    def variables_for_template(self):
        return {'my_payoff': self.participant.payoff,
                'my_decision': self.participant.decision.lower(),
                'other_player_decision': self.participant.other_player().decision.lower(),
                'same_choice': self.participant.decision == self.participant.other_player().decision}


def pages():

    return [Decision,
            ResultsWaitPage,
            Results]
