# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-otree-docs/wiki"""

from otree.db import models
import otree.models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

doc = """
Matching pennies. Single treatment. Two players are given a penny each, and will at the same time choose either heads or tails.
One player wants the outcome to match; the other wants the outcome not to match.
If the outcomes match, the former player gets both pennies; if the outcomes do not match, the latter player gets both pennies.

Source code <a href="https://github.com/wickens/otree_library/tree/master/matching_pennies" target="_blank">here</a>.
"""



class Subsession(otree.models.BaseSubsession):

    name_in_url = 'matching_pennies'


class Treatment(otree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    initial_amount = models.MoneyField(
        default=1.00,
        doc="""The value of the pennies given to each player"""
    )

class Match(otree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_match = 2


class Player(otree.models.BasePlayer):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    penny_side = models.CharField(
        choices=['heads', 'tails'],
        doc="""Heads or tails"""
    )

    def other_player(self):
        """Returns the opponent of the current player"""
        return self.other_players_in_match()[0]

    def set_payoff(self):
        """Calculates payoffs"""

        pennies_match = self.penny_side == self.other_player().penny_side

        if (self.role() == 'matcher' and pennies_match) or (self.role() == 'mismatcher' and not pennies_match):
            self.payoff = self.treatment.initial_amount * 2
        else:
            self.payoff = 0

    def role(self):
        if self.index_among_players_in_match == 1:
            return 'matcher'
        if self.index_among_players_in_match == 2:
            return 'mismatcher'


def treatments():
    return [Treatment.create()]