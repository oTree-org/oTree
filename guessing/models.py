# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-ptree-docs/wiki"""

from ptree.db import models
import ptree.models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

doc = """
Guessing Game. In this game, Participants are asked to pick a number between 0 and 100, with the winner of the contest
being the participant who is closest to 2/3 times the average number picked of all participants. In case of a tie between
the participants, the winner is picked randomly.
<p>Source code <a href="https://github.com/wickens/ptree_library/tree/master/guessing">here</a></p>
"""


class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'guessing'

    two_third_guesses = models.FloatField(default=None)

    def calculate_average(self):
        self.two_third_guesses = (2.0/3) * sum(p.guess_value for p in self.participants()) / len(self.participants())

    def choose_winner(self):
        self.calculate_average()
        winner_so_far = None
        smallest_difference_so_far = 1000 #arbitrary big number

        for p in self.participants():
            difference = abs(p.guess_value - self.two_third_guesses)
            if difference < smallest_difference_so_far:
                winner_so_far = p
                smallest_difference_so_far = difference
        winner_so_far.is_winner = True


class Treatment(ptree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    winner_payoff = models.MoneyField(
        default=1.00,
        doc='Payoff to the winner'
    )


class Match(ptree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    participants_per_match = 1


class Participant(ptree.models.BaseParticipant):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    is_winner = models.BooleanField(default=False,
        doc="""
        True if participant had the winning guess
        """
    )

    guess_value = models.PositiveIntegerField(
        default=None,
        doc="""
        Each participant guess: between 0-100
        """
    )

    def set_payoff(self):
        self.payoff = self.treatment.winner_payoff if self.is_winner else 0


def treatments():
    return [Treatment.create()]
