# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
from otree import widgets
from otree.common import Money, money_range
import random
# </standard imports>
from django_countries.fields import CountryField

class Constants:
    pass

class Subsession(otree.models.BaseSubsession):

    name_in_url = 'survey'



class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_group = 1


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    def set_payoff(self):
        """Calculate payoff, which is zero for the survey"""
        self.payoff = 0

    def q_gender_choices(self):
        return ['Male', 'Female']

    def q_age_choices(self):
        return range(13, 125)

    q_country = CountryField(verbose_name='What is your country of citizenship?')
    q_age = models.PositiveIntegerField(verbose_name='What is your age?', default=None)
    q_gender = models.CharField(default=None, verbose_name='What is your gender?', widget=widgets.RadioSelect())

    crt_bat_float = models.DecimalField(max_digits=6, decimal_places=2)
    crt_bat = models.PositiveIntegerField()
    crt_widget = models.PositiveIntegerField()
    crt_lake = models.PositiveIntegerField()


