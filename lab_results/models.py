# -*- coding: utf-8 -*-
from otree.db import models
import otree.models

doc = """
Page that shows the results of the session.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'lab_results'


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

    def set_payoff(self):
        self.payoff = 0


def treatments():

    return [Treatment.create()]
