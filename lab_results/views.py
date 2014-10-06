# -*- coding: utf-8 -*-
from __future__ import division
from lab_results._builtin import Page


class RedemptionCode(Page):

    template_name = 'lab_results/LabResults.html'

    def variables_for_template(self):
        self.player.set_payoff()
        participant = self.player.participant
        return {'base_pay': participant.session.base_pay,
                'payoff_from_subsessions': participant.payoff_from_subsessions(),
                'total_pay': participant.total_pay(),
                'redemption_code': participant.label or participant.code,}


def pages():

    return [RedemptionCode]
