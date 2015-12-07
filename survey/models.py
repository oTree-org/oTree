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

from django_countries.fields import CountryField


class Constants(BaseConstants):
    name_in_url = 'survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    def set_payoff(self):
        """Calculate payoff, which is zero for the survey"""
        self.payoff = 0

    q_country = CountryField(verbose_name='What is your country of citizenship?')
    q_age = models.PositiveIntegerField(verbose_name='What is your age?',
                                        choices=range(13, 125),
                                        initial=None)
    q_gender = models.CharField(initial=None,
                                choices=['Male', 'Female'],
                                verbose_name='What is your gender?',
                                widget=widgets.RadioSelect())

    crt_bat = models.PositiveIntegerField()
    crt_widget = models.PositiveIntegerField()
    crt_lake = models.PositiveIntegerField()


