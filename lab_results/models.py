"""Documentation at http://django-ptree.readthedocs.org/en/latest/app.html"""

from ptree.db import models
import ptree.models


doc="""
Page that shows the results of the session.
"""


class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'lab_results'


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

    def set_payoff(self):
        self.payoff = 0


def treatments():

    treatment = Treatment.create()

    return [treatment]
