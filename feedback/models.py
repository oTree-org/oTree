# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
from otree import widgets
from otree.common import Money, money_range, safe_json
import random
# </standard imports>

author = 'Your name here'

doc = """
Ask the user for their feedback on how well this game was implemented
"""

class Constants:
    name_in_url = 'feedback'
    players_per_group = 1
    number_of_rounds = 1

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
    group = models.ForeignKey(Group, null = True)
    # </built-in>

    feedback = models.CharField(
        widget=widgets.RadioSelectHorizontal(),
    )

    def feedback_choices(self):
        return Constants.feedback_choices