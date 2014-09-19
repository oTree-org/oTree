# -*- coding: utf-8 -*-
from otree.common import Money, money_range
import principal_agent.views as views
from principal_agent._builtin import Bot


class PlayerBot(Bot):

    def play(self):
        # intro
        self.submit(views.Introduction)

        if self.player.index_among_players_in_match == 1:
            self.play_1()

        else:
            self.play_2()

        # results
        self.submit(views.Results)

    def play_1(self):
        # P1 - offer
        self.submit(views.Offer,
                    {'agent_fixed_pay': 5.50,
                    'agent_return_share': 40})

    def play_2(self):
        # P2 - accept/reject
        self.submit(views.Accept, {'decision': 'Reject'})
