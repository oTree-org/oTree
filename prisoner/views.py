# -*- coding: utf-8 -*-
import prisoner.forms as forms
from prisoner.utilities import Page, MatchWaitPage, SubsessionWaitPage
from ptree.common import currency


class Decision(Page):

    """This page has the instructions and this is where the decision is made.
    Presented to both participants in a match at the same time"""

    template_name = 'prisoner/Decision.html'

    def variables_for_template(self):
        return {'friends_amount': currency(self.treatment.friends_amount),
                'betrayed_amount': currency(self.treatment.betrayed_amount),
                'enemies_amount': currency(self.treatment.enemies_amount),
                'betray_amount': currency(self.treatment.betray_amount)}

    def get_form_class(self):
        return forms.DecisionForm


class ResultsWaitPage(MatchWaitPage):

    def body_text(self):
        return 'Waiting for the other participant to make a decision.'

    def action(self):
        for p in self.match.participants():
            p.set_payoff()


class Results(Page):

    """Results page to show participants the decisions that were made and print the payoffs"""

    template_name = 'prisoner/Results.html'

    def variables_for_template(self):
        return {'my_payoff': currency(self.participant.payoff),
                'my_decision': self.participant.decision.lower(),
                'other_participant_decision': self.participant.other_participant().decision.lower(),
                'same_choice': self.participant.decision == self.participant.other_participant().decision}



def pages():

    return [Decision,
            ResultsWaitPage,
            Results]
