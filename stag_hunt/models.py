# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer

from otree import widgets
import random
from otree.common import Currency as c, currency_range

# </standard imports>


doc = """
This is a 2-player 2-strategy coordination game. The original story was from
<a href="https://en.wikipedia.org/wiki/Jean-Jacques_Rousseau" target="_blank">
    Jean-Jacques Rousseau
</a>.
"""

bibliography = (
    (
        'Skyrms, Brian. "The stag hunt." Proceedings and Addresses of the '
        'American Philosophical Association. American Philosophical '
        'Association, 2001.'
    ),
    (
        'Battalio, Raymond, Larry Samuelson, and John Van Huyck. '
        '"Optimization incentives and coordination failure in laboratory stag '
        'hunt games."Econometrica 69.3 (2001): 749-764.'
    )
)


class Constants(BaseConstants):
    name_in_url = 'stag_hunt'
    players_per_group = 2
    num_rounds = 1

    instructions_template = 'stag_hunt/Instructions.html'

    # e.g. stag_hare_payoff means:
    # "if I choose stag and the other player chooses hare, how much do I make?
    stag_stag_payoff = c(200)
    stag_hare_payoff = c(0)
    hare_stag_payoff = c(100)
    hare_hare_payoff = c(100)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    decision = models.CharField(
        choices=['Stag', 'Hare'],
        doc="""The player's choice""",
        widget=widgets.RadioSelect()
    )

    def other_player(self):
        """Returns other player in group"""
        return self.get_others_in_group()[0]

    def set_payoff(self):
        payoff_matrix = {
            'Stag': {
                'Stag': Constants.stag_stag_payoff,
                'Hare': Constants.stag_hare_payoff,
            },
            'Hare': {
                'Stag': Constants.hare_stag_payoff,
                'Hare': Constants.hare_hare_payoff,
            }
        }
        self.payoff = payoff_matrix[self.decision][
            self.other_player().decision]
