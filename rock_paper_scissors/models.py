# -*- coding: utf-8 -*-
from __future__ import division

#==============================================================================
# DOCS
#==============================================================================

"""Documentation at https://github.com/oTree-org/otree/wiki"""


#==============================================================================
# IMPORTS
#==============================================================================

import itertools

from otree.db import models
import otree.models
from otree.common import Money, money_range
from otree import widgets

#==============================================================================
# CONSTANTS
#==============================================================================

ROCK = 'Rock'
PAPER = 'Paper'
SCISSORS = 'Scissors'
RPS =  [ROCK, PAPER, SCISSORS]

TRAINING_OPTIONS = [
    {
        "options": [
            'Rock beat paper, paper beats scissors & scissors beat paper',
            'Scissors beat paper, paper beats rock & rock beat scissors',
            'Scissors beat rock, rock beats paper & paper beat rock',
        ],
        "answer": 1
    }
]


#==============================================================================
# CONF
#==============================================================================

author = 'Juan BC <jbc.develop@gmail.com>'

doc = """
<p>This is the familiar playground game "Rock-Paper-scissors".
In this implementation, players are randomly grouped in the
beginning and then continue to play against the same opponent for 3 rounds.
Their roles alters between rounds.</p>
<p>The game is preceded by one understanding question (in a real experiment,
you would often have more of these).</p>
<p>Source code <a href="https://github.com/oTree-org/oTree/tree/master/rock_paper_scissors" target="_blank">here</a>.
</p>
"""


#==============================================================================
# CLASSES
#==============================================================================

class Subsession(otree.models.BaseSubsession):

    name_in_url = 'rock_paper_scissors'

    training_1_correct = TRAINING_OPTIONS[0]["options"][TRAINING_OPTIONS[0]["answer"]]


class Group(otree.models.BaseGroup):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_group = 2

    def rps_winner(self, p1, p2):
        p1choice, p2choice = p1.rps_choice, p2.rps_choice
        if p1choice == ROCK:
            if p2choice == PAPER:
                return p2
            if p2choice == SCISSORS:
                return p1
        elif p1choice == PAPER:
            if p2choice == ROCK:
                return p1
            if p2choice == SCISSORS:
                return p2
        elif p1choice == SCISSORS:
            if p2choice == ROCK:
                return p2
            if p2choice == PAPER:
                return p1
        return None # draw

    def set_points(self):
        p1 = self.get_player_by_role('Player 1')
        p2 = self.get_player_by_role('Player 2')
        winner = self.rps_winner(p1, p2)
        if winner is p1:
            p1.points_earned = 100
            p2.points_earned = 0
            p1.is_winner = True
            p2.is_winner = False
        elif winner is p2:
            p1.points_earned = 0
            p2.points_earned = 100
            p1.is_winner = False
            p2.is_winner = True
        else:
            p2.points_earned = 0
            p1.points_earned = 0
            p2.is_winner = False
            p1.is_winner = False


class Player(otree.models.BasePlayer):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    group = models.ForeignKey(Group, null = True)
    # </built-in>


    training_question_1 = models.CharField(
        max_length=100, null=True, verbose_name='',
        widget=widgets.RadioSelect()
    )

    def training_question_1_choices(self):
        return TRAINING_OPTIONS[0]["options"]

    def is_training_question_1_correct(self):
        return self.training_question_1 == self.subsession.training_1_correct

    points_earned = models.PositiveIntegerField(
        default=0,
        doc="""Points earned"""
    )

    rps_choice = models.CharField(
        choices=RPS,
        doc="""{}, {} o {}""".format(*RPS).title(),
        widget=widgets.RadioSelect()
    )

    is_winner = models.NullBooleanField(
        doc="""Whether player won the round"""
    )

    def other_player(self):
        """Returns the opponent of the current player"""
        return self.other_players_in_group()[0]

    def role(self):
        if self.id_in_group == 1:
            return 'Player 1'
        if self.id_in_group == 2:
            return 'Player 2'

    def set_payoff(self):
        self.payoff = 0
