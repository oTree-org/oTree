# -*- coding: utf-8 -*-
from __future__ import division
"""Documentation at https://github.com/oTree-org/otree/wiki"""

from otree.db import models
import otree.models

doc = """
In this game, players are asked to pick a number within a given range.
The player wins whose guess is closest to two-thirds the average number picked by all players.
In case of a tie between players, the winner is picked at random.
Source code <a href="https://github.com/oTree-org/oTree/tree/master/guessing" target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'guessing'


class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_group = 5

    two_third_guesses = models.FloatField(default=None)

    def set_payoffs(self):
        self.two_third_guesses = (2/3) * sum([p.guess_value for p in self.get_players()]) / len(self.get_players())

        winner_so_far = None
        smallest_difference_so_far = 1000   # arbitrary big number

        for p in self.get_players():
            difference = abs(p.guess_value - self.two_third_guesses)
            if difference < smallest_difference_so_far:
                winner_so_far = p
                smallest_difference_so_far = difference
        winner_so_far.is_winner = True

        for p in self.get_players():
            if p.is_winner:
                p.payoff = p.group.winner_payoff
            else:
                p.payoff = 0

    winner_payoff = models.MoneyField(
        default=1.00,
        doc='Payoff to the winner'
    )


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    is_winner = models.BooleanField(
        default=False,
        doc="""
        True if player had the winning guess
        """
    )

    guess_value = models.PositiveIntegerField(
        default=None,
        doc="""
        Each player guess: between 0-100
        """
    )

    def guess_value_choices(self):
        return range(0, 101)


