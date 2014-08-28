# -*- coding: utf-8 -*-
from otree.db import models
import otree.models


doc = """
In this game a player is required to get a coin and flip it a number of times, while counting the number of heads.
The payoff will be calculated by the number of heads.
Source code <a href="https://github.com/oTree-org/oTree/tree/master/lying" target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):
    name_in_url = 'lying'


class Treatment(otree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    number_of_flips = models.PositiveIntegerField(default=10)
    payoff_per_head = models.MoneyField(default=0.10)


class Match(otree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_match = 1


class Player(otree.models.BasePlayer):

    subsession = models.ForeignKey(Subsession)
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)

    number_of_heads = models.PositiveIntegerField(default=None,
                                                 )

    def set_payoff(self):
        self.payoff = self.number_of_heads * self.match.treatment.payoff_per_head


def treatments():

    return [Treatment.create()]
