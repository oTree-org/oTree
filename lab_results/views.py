from lab_results.utilities import Page, MatchWaitPage, SubsessionWaitPage
from otree.common import Money, money_range
import lab_results.forms as forms

class RedemptionCode(Page):
    template_name = 'lab_results/RedemptionCode.html'

    def variables_for_template(self):
        self.participant.set_payoff()
        session_participanRENAMEt = self.participant.session_participanRENAMEt
        return {'base_pay': session_participanRENAMEt.session.base_pay,
                'payoff_from_subsessions': session_participanRENAMEt.payoff_from_subsessions(),
                'total_pay': session_participanRENAMEt.total_pay(),
                'redemption_code': session_participanRENAMEt.label or session_participanRENAMEt.code,}


def pages():
    return [RedemptionCode]