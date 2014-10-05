# -*- coding: utf-8 -*-
from __future__ import division
"""Documentation at https://github.com/oTree-org/otree/wiki"""

from otree.db import models
import otree.models
from otree import widgets

doc = """
In the symmetric matrix game, the payoffs for playing a particular strategy depend only on the other strategies employed, not on who is playing them.
Source code <a href="https://github.com/oTree-org/oTree/tree/master/matrix_symmetric" target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'matrix_symmetric'

    self_A_other_A = models.MoneyField(default=0.10)
    self_A_other_B = models.MoneyField(
        default=0.00,
        doc='''How much I make if I choose A and the other player chooses B'''
    )
    self_B_other_A = models.MoneyField(default=0.30)
    self_B_other_B = models.MoneyField(default=0.40)


class Match(otree.models.BaseMatch):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_match = 2


class Player(otree.models.BasePlayer):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    def other_player(self):
        """Returns other player in match"""
        return self.other_players_in_match()[0]

    decision = models.CharField(
        default=None,
        doc='either A or B',
        widget=widgets.RadioSelect(),
    )

    def decision_choices(self):
        return ['A', 'B']

    def set_payoff(self):

        payoff_matrix = {
            'A': {
                'A': self.subsession.self_A_other_A,
                'B': self.subsession.self_A_other_B,
            },
            'B': {
                'A': self.subsession.self_B_other_A,
                'B': self.subsession.self_B_other_B,
            }
        }

        self.payoff = payoff_matrix[self.decision][self.other_player().decision]


