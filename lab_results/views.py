# -*- coding: utf-8 -*-
from lab_results.utilities import Page


class RedemptionCode(Page):

    template_name = 'lab_results/RedemptionCode.html'

    def variables_for_template(self):
        self.participant.set_payoff()
        seq_participant = self.participant.session_participant
        return {'base_pay': seq_participant.session.base_pay,
                'payoff_from_subsessions': seq_participant.payoff_from_subsessions(),
                'total_pay': seq_participant.total_pay(),
                'redemption_code': seq_participant.label or seq_participant.code}


def pages():

    return [RedemptionCode]
