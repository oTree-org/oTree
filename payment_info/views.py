# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants
class RedemptionCode(Page):

    template_name = 'payment_info/PaymentInfo.html'

    def variables_for_template(self):
        participant = self.player.participant
        return {'fixed_pay': participant.session.fixed_pay,
                'payoff_from_subsessions': participant.payoff_from_subsessions(),
                'total_pay': participant.total_pay(),
                'redemption_code': participant.label or participant.code,}


def pages():

    return [RedemptionCode]
