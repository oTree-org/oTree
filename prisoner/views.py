# -*- coding: utf-8 -*-
import ptree.views
import ptree.views.concrete
import prisoner.forms as forms
from prisoner.utilities import ParticipantMixIn, MatchMixIn, SubsessionMixIn
from ptree.common import currency


class Decision(ParticipantMixIn, ptree.views.Page):

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


class ResultsCheckpoint(MatchMixIn, ptree.views.MatchCheckpoint):

    def wait_page_body_text(self):
        return 'Waiting for the other participant to make a decision.'

    def action(self):
        for p in self.match.participants():
            p.set_payoff()


class Results(ParticipantMixIn, ptree.views.Page):

    """Results page to show participants the decisions that were made and print the payoffs"""

    template_name = 'prisoner/Results.html'

    def variables_for_template(self):
        return {'my_payoff': currency(self.participant.payoff),
                'my_decision': self.participant.decision.lower(),
                'other_participant_decision': self.participant.other_participant().decision.lower(),
                'same_choice': True if self.participant.decision == self.participant.other_participant().decision else False}



def pages():

    return [Decision,
            ResultsCheckpoint,
            Results]
