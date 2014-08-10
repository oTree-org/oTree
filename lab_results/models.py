"""Documentation at http://django-ptree.readthedocs.org/en/latest/app.html"""

from ptree.db import models
import ptree.models


doc="""
Page that shows the results of the session.
"""


class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'lab_results'


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

    def set_payoff(self):
        self.payoff = 0


def treatments():

    return [Treatment.create()]
