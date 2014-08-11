# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-ptree-docs/wiki"""

from ptree.db import models
import ptree.models


doc = """
<p>A show case of various features that ptree support. </p>
<p>Source code <a href="https://github.com/wickens/ptree_library/tree/master/showcase">here</a></p>
"""


class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'showcase'


class Treatment(ptree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

class Match(ptree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    participants_per_match = 1


class Participant(ptree.models.BaseParticipant):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    demo_field1 = models.CharField(
        default=None,
        choices=(('yes', 'yes'), ('no', 'no')),
        doc="""
        field With radiobutton input.
        """
    )
    demo_field2 = models.TextField(
        default=None,
        doc="""
        field with textarea input
        """
    )
    demo_field3 = models.CharField(
        default=None,
        doc="""
        field with text input
        """
    )
    demo_field4 = models.CharField(
        default=None,
        choices=(('accept', 'accept'), ('reject', 'reject')),
        doc="""
        field with select choices input
        """
    )
    demo_field5 = models.PositiveIntegerField(
        default=None,
        doc="""
        field with positive integers and only odd numbers - see form validation
        """
    )

    def set_payoff(self):
        self.payoff = 0


def treatments():
    return [Treatment.create()]