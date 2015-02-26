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
This application provides a webpage instructing participants how to get paid.
Examples are given for the lab and Amazon Mechanical Turk (AMT).
"""


source_code = ""


bibliography = ()


links = {}


keywords = ()


class Constants:
    name_in_url = 'payment_info'
    players_per_group = None
    num_rounds = 1

class Subsession(otree.models.BaseSubsession):

    def before_session_starts(self):
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



