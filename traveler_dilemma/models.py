# -*- coding: utf-8 -*-
from __future__ import division
"""Documentation at https://github.com/oTree-org/otree/wiki"""
from otree.db import models
import otree.models
from otree.common import Currency as c, currency_range
from otree import widgets

doc = """
Kaushik Basu's famous traveler's dilemma (<a href="http://www.jstor.org/stable/2117865" target="_blank">AER 1994</a>). 
It is a 2-player game. 
The game is framed as a traveler's dilemma and intended for classroom/teaching use.
<br />
Source code <a href="https://github.com/oTree-org/oTree/tree/master/traveler_dilemma" target="_blank">here</a>.
"""

class Constants:
    name_in_url = 'traveler_dilemma'
    players_per_group = 2
    number_of_rounds = 1

    # Player's reward for the lowest claim"""
    reward = c(2)

    # Player's deduction for the higher claim
    penalty = c(2)

    # The maximum claim to be requested
    max_amount = c(100)

    # The minimum claim to be requested
    min_amount = c(2)

    bonus = c(10)



class Subsession(otree.models.BaseSubsession):

    pass


class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>


class Player(otree.models.BasePlayer):


    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    training_answer_mine = models.CurrencyField(
        null=True, verbose_name='My compensation would be')
    training_answer_others = models.CurrencyField(
        null=True, verbose_name="The other traveler's compensation would be")

    # claim by player
    claim = models.CurrencyField(
        doc="""
        Each player's claim
        """,
        verbose_name='Please enter a number from 2 to 100'
    )

    def claim_error_message(self, value):
        if not Constants.min_amount <= value <= Constants.max_amount:
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
