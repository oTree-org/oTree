# -*- coding: utf-8 -*-
"""Documentation at https://github.com/oTree-org/otree/wiki"""
from otree.db import models
import otree.models
from otree import forms

doc = """
<p>This is the familiar playground game "Matching Pennies". In this implementation, players are randomly matched in the
beginning and then continue to play against the same opponent. Their roles alter deterministically.</p>
<p>The game is preceded by one understanding question (in a real experiment, you would often have more of these).</p>
<p>Source code <a href="https://github.com/oTree-org/oTree/tree/master/matching_pennies" target="_blank">here</a>.</p>
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'matching_pennies'

    def pick_match_groups(self, previous_round_match_groups):
        match_groups = previous_round_match_groups
        match_groups.reverse()
        return match_groups


class Treatment(otree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    training_1_correct = 'Player 1 gets 100 points, Player 2 gets 0 points'

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

    training_question_1 = models.CharField(max_length=100, null=True, verbose_name='', widget=forms.RadioSelect())

    def training_question_1_choices(self):
        return ['Player 1 gets 0 points, Player 2 gets 0 points',
                'Player 1 gets 100 points, Player 2 gets 100 points',
                'Player 1 gets 100 points, Player 2 gets 0 points',
                'Player 1 gets 0 points, Player 2 gets 100 points']

    def is_training_question_1_correct(self):
        return self.training_question_1 == self.treatment.training_1_correct

    penny_side = models.CharField(
        choices=['Heads', 'Tails'],
        doc="""Heads or tails""",
        widget=forms.RadioSelect()
    )

    is_winner = models.NullBooleanField(
        doc='Whether the participant won this round'
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
