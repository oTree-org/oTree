# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer

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


class Constants(BaseConstants):
    name_in_url = 'payment_info'
    players_per_group = None
    num_rounds = 1

class Subsession(BaseSubsession):

    def before_session_starts(self):
        for p in self.get_players():
            p.payoff = 0



class Group(BaseGroup):
    pass

class Player(BasePlayer):
    pass


