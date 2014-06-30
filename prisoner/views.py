# -*- coding: utf-8 -*-
import ptree.views
import ptree.views.concrete
import prisoner.forms as forms
from prisoner.utilities import ParticipantMixin, ExperimenterMixin
from ptree.common import currency


class Decision(ParticipantMixin, ptree.views.Page):

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


class Results(ParticipantMixin, ptree.views.Page):

    """Results page to show participants the decisions that were made and print the payoffs"""

    template_name = 'prisoner/Results.html'

    def variables_for_template(self):
        if self.participant.payoff is None:
            self.participant.set_payoff()



        return {'my_payoff': currency(self.participant.payoff),
                'my_decision': self.participant.decision.lower(),
                'other_participant_decision': self.participant.other_participant().decision.lower(),
                'same_choice': True if self.participant.decision == self.participant.other_participant().decision else False}

    def show_skip_wait(self):
        if self.participant.other_participant().decision:
            return self.PageActions.show
        else:
            return self.PageActions.wait

    def wait_page_body_text(self):
        return 'Waiting for the other participant to make a decision.'

def pages():

    return [Decision,
            Results]
