# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-ptree-docs/wiki"""
from ptree.db import models
import ptree.models
from ptree.common import Money, money_range


doc = """
<p>
Dictator game. Single Treatment. Two players, one of whom is the dictator.
The dictator is given some amount of money, while the other participant is given nothing.
The dictator must offer part of the money to the other participant.
The offered amount cannot be rejected.
</p>

<p>Source code <a href="https://github.com/wickens/ptree_library/tree/master/dictator">here</a></p>
"""


class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'dictator'


class Treatment(ptree.models.BaseTreatment):
    subsession = models.ForeignKey(Subsession)

    allocated_amount = models.MoneyField(
        null=True,
        doc="""Initial amount allocated to the dictator"""
    )


class Match(ptree.models.BaseMatch):

    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    participants_per_match = 2

    offer_amount = models.MoneyField(
        null=True,
        doc="""Amount offered by the dictator"""
    )

    def offer_choices(self):
        """Range of allowed offers"""
        return money_range(0, self.treatment.allocated_amount, 0.05)


class Participant(ptree.models.BaseParticipant):

    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)

    def set_payoff(self):
        """Calculates player payoff"""
        if self.index_among_participants_in_match == 1:
            self.payoff = self.treatment.allocated_amount - self.match.offer_amount
        else:
            self.payoff = self.match.offer_amount


def treatments():

    return [Treatment.create(allocated_amount=1.00)]
