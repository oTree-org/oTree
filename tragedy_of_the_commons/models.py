# -*- coding: utf-8 -*-
from __future__ import division
"""Documentation at https://github.com/oTree-org/otree/wiki"""

from otree.db import models
import otree.models
from otree.common import Money, money_range
from otree import widgets

author = 'Dev'

doc = """
Tragedy of the commons.

Source code <a href="https://github.com/oTree-org/oTree/tree/master/tragedy_of_the_commons" target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'tragedy_of_the_commons'

    common_gain = models.MoneyField(
        doc="""If both players """,
        default=1.00
    )
    common_loss = models.MoneyField(
        doc="""""",
        default=0.00
    )
    individual_gain = models.MoneyField(
        doc="""""",
        default=2.00
    )
    defect_costs = models.MoneyField(
        doc="""""",
        default=0.20
    )


class Match(otree.models.BaseMatch):

    subsession = models.ForeignKey(Subsession)

    players_per_match = 2

    def set_payoffs(self):
        if all([p.decision == 'defect' for p in self.players]):
            for p in self.players:
                p.payoff = self.subsession.common_loss
        elif all([p.decision == 'cooperate' for p in self.players]):
            for p in self.players:
                p.payoff = self.subsession.common_gain
        else:
            for p in self.players:
                if p.decision == 'defect':
                    p.payoff = self.subsession.individual_gain - self.subsession.defect_costs
                else:
                    p.payoff = self.subsession.common_gain - self.subsession.defect_costs


class Player(otree.models.BasePlayer):

    match = models.ForeignKey(Match, null=True)
    subsession = models.ForeignKey(Subsession)

    def other_player(self):
        """Returns other player in match"""
        return self.other_players_in_match()[0]

    decision = models.CharField(
        null=True,
        doc="""Cooperate or defect""",
        widget=widgets.RadioSelect()
    )

    def decision_choices(self):
        return ['cooperate', 'defect']


