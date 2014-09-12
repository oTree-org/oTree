# -*- coding: utf-8 -*-
"""Documentation at https://github.com/oTree-org/otree/wiki"""

from otree.db import models
import otree.models


doc = """
<p>A show case of various features that otree support. </p>
Source code <a href="https://github.com/oTree-org/oTree/tree/master/demo_game" target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'demo_game'


class Treatment(otree.models.BaseTreatment):

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

    demo_field1 = models.CharField(
        default=None,
        choices=['yes', 'no'],
        doc="""
        field With radiobutton input.
        """
    )
    demo_field2 = models.TextField(
        default=None,
        doc="""
        field with textarea input
        """
    )
    demo_field3 = models.CharField(
        default=None,
        doc="""
        field with text input
        """
    )
    demo_field4 = models.CharField(
        default=None,
        choices=['accept', 'reject'],
        doc="""
        field with select choices input
        """
    )
    demo_field5 = models.PositiveIntegerField(
        default=None,
        doc="""
        field with positive integers and only odd numbers - see form validation
        """
    )

    def set_payoff(self):
        self.payoff = 0


def treatments():
    return [Treatment.create()]