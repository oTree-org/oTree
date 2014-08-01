# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-ptree-docs/wiki"""

from ptree.db import models
import ptree.models


doc = """
A show case of various features that ptree support.
"""


class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'showcase'


class Treatment(ptree.models.BaseTreatment):
    subsession = models.ForeignKey(Subsession)


class Match(ptree.models.BaseMatch):

    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)

    participants_per_match = 1


class Participant(ptree.models.BaseParticipant):

    match = models.ForeignKey(Match, null = True)
    treatment = models.ForeignKey(Treatment, null = True)
    subsession = models.ForeignKey(Subsession)

    demo_field1 = models.CharField(
        null=True,
        max_length=4,
        choices=(('yes', 'yes'), ('no', 'no')),
        doc="""
        field With radiobutton input.
        """
    )
    demo_field2 = models.CharField(
        null=True,
        max_length=30,
        choices=(('cooperate', 'cooperate'), ('defect', 'defect')),
        doc="""
        field with checkboxes input
        """
    )
    demo_field3 = models.TextField(
        null=True,
        doc="""
        field with textarea input
        """
    )
    demo_field4 = models.CharField(
        null=True,
        max_length=50,
        doc="""
        field with text input
        """
    )
    demo_field5 = models.CharField(
        null=True,
        max_length=10,
        choices=(('accept', 'accept'), ('reject', 'reject')),
        doc="""
        field with select choices input
        """
    )
    demo_field6 = models.PositiveIntegerField(
        null=True,
        doc="""
        field with positive integers and only odd numbers - see form validation
        """
    )

    def set_payoff(self):
        self.payoff = 0


def treatments():
    return [Treatment.create()]