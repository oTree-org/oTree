# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
from otree import widgets
from otree.common import Currency as c, currency_range
import random
# </standard imports>
from django_countries.fields import CountryField


class Constants:
    name_in_url = 'survey_sample'
    players_per_group = None
    num_rounds = 1


class Subsession(otree.models.BaseSubsession):

    pass



class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    def set_payoff(self):
        """Calculate payoff, which is zero for the survey"""
        self.payoff = 0

    q_gender = models.CharField(verbose_name='Please indicate your gender:',
                                choices=['Female', 'Male', 'Other', 'I prefer not to say'],
                                widget=widgets.RadioSelect())


