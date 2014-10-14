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
<p>This is the familiar playground game "Matching Pennies". In this implementation, players are randomly grouped in the
beginning and then continue to play against the same opponent for 3 rounds. Their roles alters between rounds.</p>
<p>The game is preceded by one understanding question (in a real experiment, you would often have more of these).</p>
<p>Source code <a href="https://github.com/oTree-org/oTree/tree/master/matching_pennies" target="_blank">here</a>.</p>
"""

class Constants:
    training_1_correct = 'Player 1 gets 100 points, Player 2 gets 0 points'

class Subsession(otree.models.BaseSubsession):

    name_in_url = 'matching_pennies'

    def next_round_groups(self, this_round_groups):
        groups = this_round_groups
        for group in groups:
            group.reverse()
        return groups




class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_group = 2

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


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    training_question_1 = models.CharField(max_length=100, null=True, verbose_name='', widget=widgets.RadioSelect())

    def training_question_1_choices(self):
        return ['Player 1 gets 0 points, Player 2 gets 0 points',
                'Player 1 gets 100 points, Player 2 gets 100 points',
                'Player 1 gets 100 points, Player 2 gets 0 points',
                'Player 1 gets 0 points, Player 2 gets 100 points']

    def is_training_question_1_correct(self):
        return self.training_question_1 == Constants.training_1_correct

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
        return self.get_others_in_group()[0]

    def role(self):
        if self.id_in_group == 1:
            return 'Player 1'
        if self.id_in_group == 2:
            return 'Player 2'

    def set_payoff(self):
        self.payoff = 0
