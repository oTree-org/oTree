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

    two_third_guesses = models.FloatField(default=None)

    def set_payoffs(self):
        self.two_third_guesses = (2.0/3) * sum([p.guess_value for p in self.players]) / len(self.players)

        winner_so_far = None
        smallest_difference_so_far = 1000   # arbitrary big number

        for p in self.players:
            difference = abs(p.guess_value - self.two_third_guesses)
            if difference < smallest_difference_so_far:
                winner_so_far = p
                smallest_difference_so_far = difference
        winner_so_far.is_winner = True

        for p in self.players:
            if p.is_winner:
                p.payoff = p.subsession.winner_payoff
            else:
                p.payoff = 0

    winner_payoff = models.MoneyField(
        default=1.00,
        doc='Payoff to the winner'
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

    players_per_match = 1


class Player(otree.models.BasePlayer):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
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


def treatments():

    return [Treatment.create()]
