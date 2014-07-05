import ptree.views
import ptree.views.concrete
from lab_results.utilities import ParticipantMixIn
from ptree.common import currency
import lab_results.forms as forms

class RedemptionCode(ParticipantMixIn, ptree.views.Page):
    template_name = 'lab_results/RedemptionCode.html'

    def variables_for_template(self):
        self.participant.set_payoff()
        seq_participant = self.participant.session_participant
        return {'base_pay': currency(seq_participant.session.base_pay),
                'payoff_from_subsessions': currency(seq_participant.payoff_from_subsessions()),
                'total_pay': currency(seq_participant.total_pay()),
                'redemption_code': seq_participant.label or seq_participant.code,}


def pages():
    return [RedemptionCode]