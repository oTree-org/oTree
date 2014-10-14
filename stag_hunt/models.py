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

class Constants:
    stag_stag_amount = Money(0.20)
    stag_hare_amount = Money(0.00)
    hare_stag_amount = Money(0.10)
    hare_hare_amount = Money(0.10)


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'stag_hunt'


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
                'Stag': Constants.stag_stag_amount,
                'Hare': Constants.stag_hare_amount,
            },
            'Hare': {
                'Stag': Constants.hare_stag_amount,
                'Hare': Constants.hare_hare_amount,
            }
        }
        self.payoff = payoff_matrix[self.decision][self.other_player().decision]


