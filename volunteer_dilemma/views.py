# -*- coding: utf-8 -*-
import ptree.views
import ptree.views.concrete
import volunteer_dilemma.forms as forms
from volunteer_dilemma.utilities import ParticipantMixIn, ExperimenterMixIn
from ptree.common import currency


class Decision(ParticipantMixIn, ptree.views.Page):

    def show_skip_wait(self):
        return self.PageActions.show

    template_name = 'volunteer_dilemma/Decision.html'

    def get_form_class(self):
        return forms.DecisionForm

    def variables_for_template(self):
        vol_ign, vol_vol, ign_vol, ign_ign = (self.treatment.general_benefit - self.treatment.volunteer_cost), \
                                            (self.treatment.general_benefit - self.treatment.volunteer_cost), \
                                            (self.treatment.general_benefit), 0
        return {
            'vol_ign': currency(vol_ign),
            'ign_vol': currency(ign_vol),
            'vol_vol': currency(vol_vol),
            'ign_ign': currency(ign_ign),
        }


class Results(ParticipantMixIn, ptree.views.Page):

    def show_skip_wait(self):
        if self.participant.other_participant().decision:
            return self.PageActions.show
        else:
            return self.PageActions.wait

    template_name = 'volunteer_dilemma/Results.html'

    def variables_for_template(self):
        if self.participant.payoff is None:
            self.participant.set_payoff()

        return {
            'decision': self.participant.decision,
            'payoff': currency(self.participant.payoff),
        }


class ExperimenterPage(ExperimenterMixIn, ptree.views.ExperimenterPage):
    pass


def pages():
    return [
        Decision,
        Results
    ]