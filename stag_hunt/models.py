# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
from otree import widgets
from otree.common import Money, money_range
import random
# </standard imports>


doc = """
This is a 2-player 2-strategy coordination game. The original story was from <a href="https://en.wikipedia.org/wiki/Jean-Jacques_Rousseau" target="_blank">Jean-Jacques Rousseau</a>.
<br />
Source code <a href="https://github.com/oTree-org/oTree/tree/master/stag_hunt" target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'stag_hunt'

    stag_stag_amount = models.MoneyField(
        default=0.20,
        doc="""Payoff if both players choose stag"""
    )

    stag_hare_amount = models.MoneyField(
        default=0.00,
        doc="""Payoff if the player chooses stag but the other hare"""
    )

    hare_stag_amount = models.MoneyField(
        default=0.10,
        doc="""Payoff if the player chooses hare but the other stag"""
    )

    hare_hare_amount = models.MoneyField(
        default=0.10,
        doc="""Payoff if both players choose hare"""
    )




class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_group = 2


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    decision = models.CharField(
        default=None,
        doc="""The player's choice""",
        widget=widgets.RadioSelect()
    )

    def decision_choices(self):
        return ['Stag', 'Hare']

    def other_player(self):
        """Returns other player in group"""
        return self.get_others_in_group()[0]

    def set_payoff(self):

        payoff_matrix = {
            'Stag': {
                'Stag': self.subsession.stag_stag_amount,
                'Hare': self.subsession.stag_hare_amount,
            },
            'Hare': {
                'Stag': self.subsession.hare_stag_amount,
                'Hare': self.subsession.hare_hare_amount,
            }
        }
        self.payoff = payoff_matrix[self.decision][self.other_player().decision]


