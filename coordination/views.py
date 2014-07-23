# -*- coding: utf-8 -*-
import ptree.views
import ptree.views.concrete
import coordination.forms as forms
from coordination.utilities import ParticipantMixIn, MatchMixIn
from ptree.common import currency


class Introduction(ParticipantMixIn, ptree.views.Page):

    def participate_condition(self):
        return True

    template_name = 'coordination/Introduction.html'

    def variables_for_template(self):
        return {
            'similar_amount': currency(self.treatment.similar_amount),
            'dissimilar_amount': currency(self.treatment.dissimilar_amount),
        }


class Choice(ParticipantMixIn, ptree.views.Page):

    def participate_condition(self):
        return True

    template_name = 'coordination/Choice.html'

    def get_form_class(self):
        return forms.ChoiceForm


class ResultsCheckpoint(MatchMixIn, ptree.views.MatchCheckpoint):

    def action(self):
        for p in self.match.participants():
            p.set_payoff()

    def wait_page_body_text(self):
        return "Waiting for the other participant."


class Results(ParticipantMixIn, ptree.views.Page):

    def participate_condition(self):
        return True

    template_name = 'coordination/Results.html'

    def variables_for_template(self):
        return {
            'payoff': currency(self.participant.payoff),
            'choice': self.participant.choice,
            'other_choice': self.participant.other_participant().choice
        }


def pages():
    return [
        Introduction,
        Choice,
        ResultsCheckpoint,
        Results
    ]