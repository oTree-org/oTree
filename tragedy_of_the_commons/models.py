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

class Constants:
    common_gain = Money(0.10)
    common_loss = Money(0.00)
    individual_gain = Money(2.00)
    defect_costs = Money(0.20)

class Subsession(otree.models.BaseSubsession):

    name_in_url = 'tragedy_of_the_commons'


class Group(otree.models.BaseGroup):

    subsession = models.ForeignKey(Subsession)

    players_per_group = 2

    def set_payoffs(self):
        players = self.get_players()
        if all([p.decision == 'defect' for p in players]):
            for p in players:
                p.payoff = Constants.common_loss
        elif all([p.decision == 'cooperate' for p in players]):
            for p in players:
                p.payoff = Constants.common_gain
        else:
            for p in players:
                if p.decision == 'defect':
                    p.payoff = Constants.individual_gain - Constants.defect_costs
                else:
                    p.payoff = Constants.common_gain - Constants.defect_costs


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


