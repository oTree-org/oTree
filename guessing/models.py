# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-otree-docs/wiki"""

from otree.db import models
import otree.models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

doc = """
Guessing Game. In this game, Players are asked to pick a number between 0 and 100, with the winner of the contest
being the player who is closest to 2/3 times the average number picked of all players. In case of a tie between
the players, the winner is picked randomly.
<p>Source code <a href="https://github.com/wickens/otree_library/tree/master/guessing">here</a></p>
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'guessing'

    two_third_guesses = models.FloatField(default=None)

    def calculate_average(self):
        self.two_third_guesses = (2.0/3) * sum(p.guess_value for p in self.players) / len(self.players)

    def choose_winner(self):
        self.calculate_average()
        winner_so_far = None
        smallest_difference_so_far = 1000 #arbitrary big number

        for p in self.players:
            difference = abs(p.guess_value - self.two_third_guesses)
            if difference < smallest_difference_so_far:
                winner_so_far = p
                smallest_difference_so_far = difference
        winner_so_far.is_winner = True

        for p in self.players:
            if p.is_winner:
                p.payoff = p.treatment.winner_payoff
            else:
                p.payoff = 0


class Treatment(otree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    winner_payoff = models.MoneyField(
        default=1.00,
        doc='Payoff to the winner'
    )


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

    is_winner = models.BooleanField(default=False,
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


def treatments():
    return [Treatment.create()]
