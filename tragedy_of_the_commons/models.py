# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
from otree import widgets
from otree.common import Money, money_range
import random
# </standard imports>

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


class Group(otree.models.BaseGroup):

    subsession = models.ForeignKey(Subsession)

    players_per_group = 2

    def set_payoffs(self):
        if all([p.decision == 'defect' for p in self.get_players()]):
            for p in self.get_players():
                p.payoff = self.subsession.common_loss
        elif all([p.decision == 'cooperate' for p in self.get_players()]):
            for p in self.get_players():
                p.payoff = self.subsession.common_gain
        else:
            for p in self.get_players():
                if p.decision == 'defect':
                    p.payoff = self.subsession.individual_gain - self.subsession.defect_costs
                else:
                    p.payoff = self.subsession.common_gain - self.subsession.defect_costs


class Player(otree.models.BasePlayer):

    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)

    def other_player(self):
        """Returns other player in group"""
        return self.get_others_in_group()[0]

    decision = models.CharField(
        null=True,
        doc="""Cooperate or defect""",
        widget=widgets.RadioSelect()
    )

    def decision_choices(self):
        return ['cooperate', 'defect']


