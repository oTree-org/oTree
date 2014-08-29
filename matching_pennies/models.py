# -*- coding: utf-8 -*-
"""Documentation at https://github.com/oTree-org/otree/wiki"""
from otree.db import models
import otree.models

doc = """
Matching pennies. Single treatment. Two players are given a penny each, and will at the same time choose either heads or tails.
One player wants the outcome to match; the other wants the outcome not to match.
If the outcomes match, the former player gets both pennies; if the outcomes do not match, the latter player gets both pennies.
Source code <a href="https://github.com/oTree-org/oTree/tree/master/matching_pennies" target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'matching_pennies'


class Treatment(otree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    initial_amount = models.MoneyField(
        default=0.10,
        doc="""The value of the pennies given to each player"""
    )


class Match(otree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_match = 2

    def set_payoffs(self):
        matcher = self.get_player_by_role('matcher')
        mismatcher = self.get_player_by_role('mismatcher')

        if matcher.penny_side == mismatcher.penny_side:
            matcher.payoff = self.treatment.initial_amount*2
            mismatcher.payoff = 0
            matcher.is_winner = True
            mismatcher.is_winner = False
        else:
            matcher.payoff = 0
            mismatcher.payoff = self.treatment.initial_amount*2
            matcher.is_winner = False
            mismatcher.is_winner = True


class Player(otree.models.BasePlayer):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    penny_side = models.CharField(
        choices=['Heads', 'Tails'],
        doc="""Heads or tails"""
    )

    is_winner = models.NullBooleanField(
        doc='Whether the participant won this round'
    )

    def other_player(self):
        """Returns the opponent of the current player"""
        return self.other_players_in_match()[0]

    def role(self):
        if self.index_among_players_in_match == 1:
            return 'matcher'
        if self.index_among_players_in_match == 2:
            return 'mismatcher'


def treatments():

    return [Treatment.create()]