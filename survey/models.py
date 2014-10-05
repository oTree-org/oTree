# -*- coding: utf-8 -*-
from __future__ import division
from django_countries.fields import CountryField
from otree.db import models
import otree.models
from otree import widgets


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'survey'



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
        """Calculate payoff, which is zero for the survey"""
        self.payoff = 0

    def q_gender_choices(self):
        return ['Male', 'Female']

    def q_age_choices(self):
        return range(13, 125)

    q_country = CountryField(default=None, verbose_name='What is your country of citizenship?')
    q_age = models.PositiveIntegerField(verbose_name='What is your age?', default=None)
    q_gender = models.CharField(default=None, verbose_name='What is your gender?', widget=widgets.RadioSelect())

    crt_bat_float = models.DecimalField(default=None, max_digits=6, decimal_places=2)
    crt_bat = models.PositiveIntegerField(default=None)
    crt_widget = models.PositiveIntegerField(default=None)
    crt_lake = models.PositiveIntegerField(default=None)


def treatments():

    return [Treatment.create()]
