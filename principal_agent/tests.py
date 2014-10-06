# -*- coding: utf-8 -*-
from __future__ import division
from otree.common import Money, money_range
import principal_agent.views as views
from principal_agent._builtin import Bot
import random


class PlayerBot(Bot):

    def play(self):
        # intro
        self.submit(views.Introduction)

        if self.player.id_in_group == 1:
            self.play_1()

        else:
            self.play_2()

        # results
        self.submit(views.Results)

    def play_1(self):
        # P1/A - propose contract

        fixed_pay = random.choice(money_range(-self.subsession.max_fixed_payment, self.subsession.max_fixed_payment, 0.50))
        return_share = random.choice([x/100.0 for x in range(10, 110, 10)])

        self.submit(views.Offer,
                    {'agent_fixed_pay': fixed_pay,
                     'agent_return_share': return_share})

    def play_2(self):
        # P2/B - accept or reject contract

        self.submit(views.Accept, {'contract_accepted': random.choice([True, False])})

        # effort level only if contract is accepted
        if self.group.contract_accepted:
            self.submit(views.WorkEffort, {'agent_work_effort': random.choice(range(1, 11))})
