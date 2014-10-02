# -*- coding: utf-8 -*-
"""Documentation at https://github.com/oTree-org/otree/wiki"""

from otree.db import models
import otree.models
from otree.common import Money, money_range

author = 'Dev'

doc = """
Tragedy of the commons.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'tragedy_of_the_commons'


class Treatment(otree.models.BaseTreatment):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    common_share = models.MoneyField(null=True, doc='''Amount to be shared by all participants''')


class Match(otree.models.BaseMatch):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    treatment = models.ForeignKey(Treatment)
    # </built-in>

    players_per_match = 2

    def calculate_total_hours(self):
        return sum(p.hours_fished for p in self.players)

    def set_payoffs(self):
        # TODO: re-do the payoff calculation
        for p in self.players:
            per_hour_gain = self.treatment.common_share / self.calculate_total_hours()
            p.payoff = per_hour_gain * p.hours_fished


class Player(otree.models.BasePlayer):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    treatment = models.ForeignKey(Treatment, null = True)
    match = models.ForeignKey(Match, null = True)
    # </built-in>

    hours_fished = models.PositiveIntegerField(
        default=None,
        doc="""
        Participant's hours to fish.
        """
    )


def treatments():
    return [Treatment.create(
        common_share = 20.00
    )]