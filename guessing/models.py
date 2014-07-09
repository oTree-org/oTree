# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-ptree-docs/wiki"""

from ptree.db import models
import ptree.models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

doc = """
<p>In Guessing Game, Participants are asked to pick a number between 0 and 100, with the winner of the contest
being the participant that is closest to 2/3 times the average number picked of all participants.
</p>

<p>Source code <a href="https://github.com/wickens/ptree_library/tree/master/guessing">here</a></p>
"""


class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'guessing'


class Treatment(ptree.models.BaseTreatment):
    subsession = models.ForeignKey(Subsession)


class Match(ptree.models.BaseMatch):

    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)

    average_guesses = models.FloatField(null=True)

    participants_per_match = 1

    def calculate_average(self):
        self.average_guesses = sum(p.guess_value for p in self.subsession.participants()) / len(self.subsession.participants())
        print self.average_guesses


class Participant(ptree.models.BaseParticipant):

    match = models.ForeignKey(Match, null = True)
    treatment = models.ForeignKey(Treatment, null = True)
    subsession = models.ForeignKey(Subsession)

    guess_value = models.PositiveIntegerField(
        null=True,
        doc="""
        Each participant guess: between 0-100
        """
    )

    def set_payoff(self):
        #TODO: FIX THIS- No payoff for now
        self.payoff = 0


def treatments():

    treatment_list = []

    treatment = Treatment(
    )

    treatment_list.append(treatment)

    return treatment_list