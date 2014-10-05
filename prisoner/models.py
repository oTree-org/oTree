# -*- coding: utf-8 -*-
from __future__ import division
from otree.db import models
import otree.models
from otree import widgets

doc = """
This is a one-shot prisoner dilemma game. Two players are asked separately whether they want to cooperate or defect.
Their choices directly determine the payoffs.
<br/ >
Source code <a href="https://github.com/oTree-org/oTree/tree/master/prisoner" target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'prisoner'

    betray_amount = models.MoneyField(
        doc="""amount a player makes if he chooses 'defect' and the other chooses 'cooperate'""",
        default=0.30,
    )

    friend_amount = models.MoneyField(
        doc="""amount both players make if both choose 'cooperate'""",
        default=0.20,
    )
    betrayed_amount = models.MoneyField(
        doc="""amount a player makes if he chooses 'cooperate' and the other chooses 'defect'""",
        default=0.10,
    )

    enemy_amount = models.MoneyField(
        doc="""amount both players make if both choose 'defect'""",
        default=0.00,
    )




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

    decision = models.CharField(
        default=None,
        doc="""This player's decision""",
        widget=widgets.RadioSelect()
    )

    def decision_choices(self):
        return ['Cooperate', 'Defect']

    def other_player(self):
        """Returns other player in match"""
        return self.other_players_in_match()[0]

    def set_payoff(self):
        """Calculate player payoff"""
        payoff_matrix = {'Cooperate': {'Cooperate': self.subsession.friend_amount,
                                       'Defect': self.subsession.betrayed_amount},
                         'Defect':   {'Cooperate': self.subsession.betray_amount,
                                      'Defect': self.subsession.enemy_amount}}

        self.payoff = (payoff_matrix[self.decision]
                                    [self.other_player().decision])



