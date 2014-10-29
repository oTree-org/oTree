# -*- coding: utf-8 -*-
from __future__ import division
from . import views
from ._builtin import Bot


class PlayerBot(Bot):

    def play(self):
        # intro
        self.submit(views.Introduction)
        self.submit(views.Question1, {'training_my_payoff': 1,
                                      'training_other_payoff': 2})
        self.submit(views.Feedback1)

        if self.player.id_in_group == 1:
            self.play_1()

        else:
            self.play_2()

        # results
        self.submit(views.Results)
        if self.player.id_in_group == 1:
            assert self.player.payoff == 46 + 30, self.player.payoff
        else:
            assert self.player.payoff == 34 + 30, self.player.payoff
        self.submit(views.FeedbackQ, {'feedback': 4})

    def play_1(self):
        # P1/A - propose contract
        self.submit(views.Offer, {'agent_fixed_pay': 10,
                                  'agent_return_share': 0.6})

    def play_2(self):
        # P2/B - accept or reject contract
        self.submit(views.Accept, {'contract_accepted': True,
                                   'agent_work_effort': 10})
