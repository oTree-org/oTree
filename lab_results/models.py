# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
from otree import widgets
from otree.common import Currency as c, currency_range
import random
# </standard imports>


doc = """
Page that shows the results of the session.
"""

class Constants:
    name_in_url = 'lab_results'
    players_per_group = 1
    number_of_rounds = 1

class Subsession(otree.models.BaseSubsession):

    def initialize(self):
        for p in self.get_players():
            p.payoff = 0



class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>



