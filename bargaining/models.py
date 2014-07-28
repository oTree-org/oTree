# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-ptree-docs/wiki"""

from ptree.db import models
import ptree.models
from ptree.common import currency


doc = """
<p>
The Bargaining Game is a two-player game used to model bargaining interactions. In this game,
two players demand a portion of some amount of money. If the total amount
requested by the players is less than that available, both players get their request.
If their total request is greater than that available, neither player gets their request.
</p>

<p>Source code <a href="https://github.com/wickens/ptree_library/tree/master/bargaining">here</a></p>
"""


class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'bargaining'


class Treatment(ptree.models.BaseTreatment):
    subsession = models.ForeignKey(Subsession)

    amount_shared = models.PositiveIntegerField(null=True,
        doc="""
        Amount to be shared by both players
        """
    )


class Match(ptree.models.BaseMatch):

    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)

    participants_per_match = 2

    def request_choices(self):
        """Range of allowed request amount"""
        return range(0, self.treatment.amount_shared + 1, 5)

    def get_request_field_choices(self):
        """Tuple of tuples with allowed request amount"""
        return tuple([(i, currency(i)) for i in self.request_choices()])


class Participant(ptree.models.BaseParticipant):

    match = models.ForeignKey(Match, null = True)
    treatment = models.ForeignKey(Treatment, null = True)
    subsession = models.ForeignKey(Subsession)

    request_amount = models.PositiveIntegerField(
        null=True,
        doc="""
        Amount requested by each participant..
        """
    )

    def other_participant(self):
        """Returns the opponent of the current player"""
        return self.other_participants_in_match()[0]

    def set_payoff(self):
        if self.request_amount + self.other_participant().request_amount <= self.treatment.amount_shared:
            self.payoff = self.request_amount
        else:
            self.payoff = 0


def treatments():

    return [Treatment.create(amount_shared=100)]
