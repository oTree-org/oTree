"""Documentation at http://django-ptree.readthedocs.org/en/latest/app.html"""

from ptree.db import models
import ptree.models


doc="""
In this game you are required to get a coin and flip it a number of times, while counting the number of heads
you get. The payoff will be calculated by the number of heads that comes up.

<p>Source code <a href="https://github.com/wickens/ptree_library/tree/master/lying">here</a></p>
"""


class Subsession(ptree.models.BaseSubsession):
    name_in_url = 'lying'


class Treatment(ptree.models.BaseTreatment):
    subsession = models.ForeignKey(Subsession)
    number_of_flips = models.PositiveIntegerField()
    payoff_per_head = models.PositiveIntegerField()


class Match(ptree.models.BaseMatch):

    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)

    participants_per_match = 1


class Participant(ptree.models.BaseParticipant):

    subsession = models.ForeignKey(Subsession)
    match = models.ForeignKey(Match, null = True)
    treatment = models.ForeignKey(Treatment, null = True)

    number_of_heads = models.PositiveIntegerField(null = True, blank=False)

    def set_payoff(self):
        self.payoff = self.number_of_heads * self.match.treatment.payoff_per_head


def treatments():

    treatment = Treatment.create(
        number_of_flips = 10,
        payoff_per_head = 10,
    )

    return [treatment]