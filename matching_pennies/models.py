# -*- coding: utf-8 -*-
from __future__ import division
"""Documentation at https://github.com/oTree-org/otree/wiki"""
from otree.db import models
import otree.models
from otree import widgets

doc = """
<p>This is the familiar playground game "Matching Pennies". In this implementation, players are randomly matched in the
beginning and then continue to play against the same opponent for 3 rounds. Their roles might alter across rounds.</p>
<p>The game is preceded by one understanding question (in a real experiment, you would often have more of these).</p>
<p>Source code <a href="https://github.com/oTree-org/oTree/tree/master/matching_pennies" target="_blank">here</a>.</p>
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'matching_pennies'

    def pick_match_groups(self, previous_round_match_groups):
        match_groups = previous_round_match_groups
        for group in match_groups:
            group.reverse()
        return match_groups

    training_1_correct = 'Player 1 gets 100 points, Player 2 gets 0 points'

    point_value = models.MoneyField(
        default=0.01,
        doc="""Monetary value of each game point"""
    )


class Treatment(otree.models.BaseTreatment):
    """Leave this class empty"""

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>



class Match(otree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_match = 2

    def set_points(self):
        p1 = self.get_player_by_role('Player 1')
        p2 = self.get_player_by_role('Player 2')

        if p2.penny_side == p1.penny_side:
            p2.points_earned = 100
            p1.points_earned = 0
            p2.is_winner = True
            p1.is_winner = False
        else:
            p2.points_earned = 0
            p1.points_earned = 100
            p2.is_winner = False
            p1.is_winner = True

    def set_payoffs(self):
        for player in self.players:
            player.payoff = sum(p.points_earned for p in player.me_in_previous_rounds() + [player]) * self.subsession.point_value


class Player(otree.models.BasePlayer):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    training_question_1 = models.CharField(max_length=100, null=True, verbose_name='', widget=widgets.RadioSelect())

    def training_question_1_choices(self):
        return ['Player 1 gets 0 points, Player 2 gets 0 points',
                'Player 1 gets 100 points, Player 2 gets 100 points',
                'Player 1 gets 100 points, Player 2 gets 0 points',
                'Player 1 gets 0 points, Player 2 gets 100 points']

    def is_training_question_1_correct(self):
        return self.training_question_1 == self.subsession.training_1_correct

    points_earned = models.PositiveIntegerField(
        default=0,
        doc="""Points earned"""
    )

    penny_side = models.CharField(
        choices=['Heads', 'Tails'],
        doc="""Heads or tails""",
        widget=widgets.RadioSelect()
    )

    is_winner = models.NullBooleanField(
        doc="""Whether player won the round"""
    )

    def other_player(self):
        """Returns the opponent of the current player"""
        return self.other_players_in_match()[0]

    def role(self):
        if self.index_among_players_in_match == 1:
            return 'Player 1'
        if self.index_among_players_in_match == 2:
            return 'Player 2'


def treatments():

    return [Treatment.create()]
