# -*- coding: utf-8 -*-
from __future__ import division
from . import views
from ._builtin import Bot
import random
from otree.common import Money, money_range
import time
from .models import Constants

def sleep_seconds():
    return random.choice(range(5, 30, 1))


class PlayerBot(Bot):

    def play(self):
        # intro
        time.sleep(5)
        self.submit(views.Introduction)

        if self.player.id_in_group == 1:
            self.play_1()

        else:
            self.play_2()

        # results
        time.sleep(sleep_seconds())
        self.submit(views.Results)

    def play_1(self):
        # P1/A - propose contract
        fixed_pay = random.choice(money_range(-Constants.max_fixed_payment, Constants.max_fixed_payment, 0.50))
        return_share = random.choice([x/100.0 for x in range(10, 110, 10)])

        time.sleep(sleep_seconds())
        self.submit(views.Offer,
                    {'agent_fixed_pay': fixed_pay,
                     'agent_return_share': return_share})

    def play_2(self):
        # P2/B - accept or reject contract

        time.sleep(sleep_seconds())
        self.submit(views.Accept, {'contract_accepted': random.choice([True, False])})

        # effort level only if contract is accepted
        time.sleep(sleep_seconds())
        if self.group.contract_accepted:
            self.submit(views.WorkEffort, {'agent_work_effort': random.choice(range(1, 11))})
