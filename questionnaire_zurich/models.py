# -*- coding: utf-8 -*-
from django_countries import CountryField
from ptree.db import models
import ptree.models


class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'questionnaire_zurich'


class Treatment(ptree.models.BaseTreatment):

    subsession = models.ForeignKey(Subsession)


class Match(ptree.models.BaseMatch):

    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    participants_per_match=1


class Participant(ptree.models.BaseParticipant):

    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)

    finished_questionnaire = models.BooleanField(default=False)

    def set_payoff(self):
        self.payoff = 0

    GENDER_CHOICES = (('Male', 'Male'),
                      ('Female', 'Female'))


    RELIGION_CHOICES = (
        ('Secular/Agnostic/Atheist', 'Secular/Agnostic/Atheist'),
        ('Christianity: Catholic', 'Christianity: Catholic'),
        ('Christianity: Protestant', 'Christianity: Protestant'),
        ('Christianity: Orthodox', 'Christianity: Orthodox'),
        ('Christianity: New Apostolic', 'Christianity: New Apostolic'),
        ('Islam', 'Islam'),
        ('Hinduism', 'Hinduism'),
        ('Buddhism', 'Buddhism'),
        ('Judaism', 'Judaism'),
        ('Other', 'Other'),
    )

    YES_NO_CHOICES = (
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('Unsure/Decline to answer', 'Unsure/Decline to answer')
    )

    STUDY_CHOICES = (
        ('Law', 'Law'),
        ('Economics', 'Economics'),
        ('Medicine', 'Medicine'),
        ('Psychology', 'Psychology'),
        ('Social Sciences', 'Social Sciences'),
        ('Humanities', 'Humanities'),
        ('Liberal Arts', 'Liberal Arts'),
        ('Natural Sciences', 'Natural Sciences'),
        ('Mathematics/Physics', 'Mathematics/Physics'),
        ('Engineering/Computer Science', 'Engineering/Computer Science'),
        ('Other', 'Other')
    )

    PARTY_CHOICES = (
        ('Did not vote', 'Did not vote'),
        ('Conservative Democratic Party', 'Conservative Democratic Party'),
        ('Christian Democratic Party', 'Christian Democratic Party'),
        ('The Liberals', 'The Liberals'),
        ('Green Liberals', 'Green Liberals'),
        ('Greens', 'Greens'),
        ('Social Democrats', 'Social Democrats'),
        ("People's Party", "People's Party"),
        ('Other', 'Other')
    )

    q_country = CountryField(null=True, verbose_name='What is your country of citizenship?')
    q_age = models.PositiveIntegerField(verbose_name='What is your age?', null=True)
    q_gender = models.CharField(max_length=100,choices=GENDER_CHOICES, null=True, verbose_name='What is your gender?')
    q_study = models.CharField(max_length=100, choices=STUDY_CHOICES, null=True, verbose_name='What is your field of study?')
    q_party = models.CharField(max_length=100, choices=PARTY_CHOICES, null=True, verbose_name='For which party did you vote in the 2013 German federal elections?')
    q_religion = models.CharField(max_length=100,choices=RELIGION_CHOICES, null=True, verbose_name='What is your religion?')
    q_religion_count = models.PositiveIntegerField(verbose_name='On average, how often per month to you do attend religious services?', null=True)
    q_volunteer = models.CharField(max_length=100, choices=YES_NO_CHOICES, null=True,
                                      verbose_name='During the last year, have you volunteered time for a non-profit organization?')
    q_donate = models.CharField(max_length=100, choices=YES_NO_CHOICES, null=True,
                                   verbose_name='During the last year, have you donated money to a non-profit organization?')
    crt_doctor = models.PositiveIntegerField(null=True)
    crt_meal_float = models.DecimalField(null=True, max_digits=6, decimal_places=2)
    crt_meal = models.PositiveIntegerField(null=True)
    crt_run = models.PositiveIntegerField(null=True)
    crt_seen_before_new = models.CharField(max_length=20, choices=YES_NO_CHOICES, verbose_name='Have you seen these questions before?', null=True)

    crt_bat_float = models.DecimalField(null=True, max_digits=6, decimal_places=2)
    crt_bat = models.PositiveIntegerField(null=True)
    crt_widget = models.PositiveIntegerField(null=True)
    crt_lake = models.PositiveIntegerField(null=True)
    crt_seen_before_old = models.CharField(max_length=20, choices=YES_NO_CHOICES, verbose_name='Have you seen these questions before?', null=True)


def treatments():

    treatment = Treatment.create()
    return [treatment]
