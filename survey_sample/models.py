# -*- coding: utf-8 -*-
from __future__ import division
from django_countries.fields import CountryField
from otree.db import models
import otree.models
from otree import widgets


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'survey_sample'


class Treatment(otree.models.BaseTreatment):
    """Leave this class empty"""

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>


class Match(otree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_match = 1


class Player(otree.models.BasePlayer):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    def set_payoff(self):
        """Calculate payoff, which is zero for the survey"""
        self.payoff = 0

    def q_gender_choices(self):
        return ['Female', 'Male', 'Other', 'I prefer not to say']

    q_gender = models.CharField(default=None, verbose_name='Please indicate your gender:', widget=widgets.RadioSelect())


def treatments():

    return [Treatment.create()]
