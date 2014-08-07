# -*- coding: utf-8 -*-
from django_countries.fields import CountryField
from ptree.db import models
import ptree.models

class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'survey'


class Treatment(ptree.models.BaseTreatment):

    subsession = models.ForeignKey(Subsession)


class Match(ptree.models.BaseMatch):

    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    participants_per_match = 1


class Participant(ptree.models.BaseParticipant):

    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)

    def set_payoff(self):
        """Calculate payoff, which is zero for the survey"""
        self.payoff = 0

    q_country = CountryField(null=True, verbose_name='What is your country of citizenship?')
    q_age = models.PositiveIntegerField(verbose_name='What is your age?', null=True)
    q_gender = models.CharField(max_length=100, choices=['Male','Female'], null=True, verbose_name='What is your gender?')

    crt_bat_float = models.DecimalField(null=True, max_digits=6, decimal_places=2)
    crt_bat = models.PositiveIntegerField(null=True)
    crt_widget = models.PositiveIntegerField(null=True)
    crt_lake = models.PositiveIntegerField(null=True)


def treatments():

    treatment = Treatment.create()

    return [treatment]
