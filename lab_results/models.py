# -*- coding: utf-8 -*-
from __future__ import division
from otree.db import models
import otree.models

doc = """
Page that shows the results of the session.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'lab_results'



class Match(otree.models.BaseMatch):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_match = 1


class Player(otree.models.BasePlayer):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    def set_payoff(self):
        self.payoff = 0


def treatments():

    return [Treatment.create()]
