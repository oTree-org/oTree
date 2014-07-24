# -*- coding: utf-8 -*-
import ptree.views
import ptree.views.concrete
import volunteer_dilemma.forms as forms
from volunteer_dilemma.utilities import ParticipantMixIn, MatchMixIn, SubsessionMixIn
from ptree.common import currency


class Decision(ParticipantMixIn, ptree.views.Page):

    template_name = 'volunteer_dilemma/Decision.html'

    def get_form_class(self):
        return forms.DecisionForm

    def variables_for_template(self):
        vol_ign = self.treatment.general_benefit - self.treatment.volunteer_cost
        vol_vol = self.treatment.general_benefit - self.treatment.volunteer_cost
        ign_vol = self.treatment.general_benefit
        ign_ign = 0

        return {
            'vol_ign': currency(vol_ign),
            'ign_vol': currency(ign_vol),
            'vol_vol': currency(vol_vol),
            'ign_ign': currency(ign_ign),
        }

class ResultsCheckpoint(MatchMixIn, ptree.views.MatchCheckpoint):

    def action(self):
        for p in self.match.participants():
            p.set_payoff()

class Results(ParticipantMixIn, ptree.views.Page):

    template_name = 'volunteer_dilemma/Results.html'

    def variables_for_template(self):
        return {
            'decision': self.participant.decision,
            'payoff': currency(self.participant.payoff),
        }

def pages():
    return [
        Decision,
        ResultsCheckpoint,
        Results
    ]