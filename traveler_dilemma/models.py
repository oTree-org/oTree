# -*- coding: utf-8 -*-
from __future__ import division
"""Documentation at https://github.com/oTree-org/otree/wiki"""
from otree.db import models
import otree.models
from otree.common import money_range
from otree import widgets

doc = """
Kaushik Basu's famous traveler's dilemma (<a href="http://www.jstor.org/stable/2117865" target="_blank">AER 1994</a>). 
It is a 2-player game. 
The game is framed as a traveler's dilemma and intended for classroom/teaching use.
<br />
Source code <a href="https://github.com/oTree-org/oTree/tree/master/traveler_dilemma" target="_blank">here</a>.
"""

class Constants:
    # Player's reward for the lowest claim"""
    reward = 2

    # Player's deduction for the higher claim
    penalty = 2

    # The maximum claim to be requested
    max_amount = 100

    # The minimum claim to be requested
    min_amount = 2

    bonus = 10



class Subsession(otree.models.BaseSubsession):

    name_in_url = 'traveler_dilemma'


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

    training_answer_mine = models.PositiveIntegerField(
        null=True, verbose_name='My compensation would be')
    training_answer_others = models.PositiveIntegerField(
        null=True, verbose_name="The other traveler's compensation would be")

    # claim by player
    claim = models.PositiveIntegerField(
        doc="""
        Each player's claim
        """,
        verbose_name='Please enter a number from 2 to 100'
    )
    feedback = models.PositiveIntegerField(
        choices=(
            (5, 'Very well'),
            (4, 'Well'),
            (3, 'OK'),
            (2, 'Badly'),
            (1, 'Very badly')), widget=widgets.RadioSelectHorizontal(),
        verbose_name='')

    def claim_error_message(self, value):
        if not Constants.min_amount\
                <= value <= Constants.max_amount:
            return 'Your entry is invalid.'

    def other_player(self):
        return self.get_others_in_group()[0]

    def set_payoff(self):
        other = self.other_player().claim
        if self.claim < other:
            self.payoff = Constants.bonus + self.claim + Constants.reward
        elif self.claim > other:
            self.payoff = Constants.bonus + other - Constants.penalty
        else:
            self.payoff = Constants.bonus + self.claim
