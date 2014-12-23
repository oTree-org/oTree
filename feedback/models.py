# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json
import random
# </standard imports>

author = 'Your name here'

doc = """
Ask the user for their feedback on how well this game was implemented
"""

source_code = ""


bibliography = ()


links = {}


keywords = ()


class Constants:
    name_in_url = 'feedback'
    players_per_group = None
    num_rounds = 1

    feedback_choices = ['Very well', 'Well', 'OK', 'Badly', 'Very badly']


class Subsession(otree.models.BaseSubsession):
    pass


class Group(otree.models.BaseGroup):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>


class Player(otree.models.BasePlayer):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    group = models.ForeignKey(Group, null=True)
    # </built-in>

    feedback = models.CharField(
        choices=Constants.feedback_choices,
        widget=widgets.RadioSelectHorizontal(),
    )
