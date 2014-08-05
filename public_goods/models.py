# -*- coding: utf-8 -*-
from ptree.db import models
import ptree.models
from ptree.common import Money, money_range


doc = """
Public goods game. Single treatment. Four players can contribute to a joint project.
The total contribution is multiplied by some factor, the resulting amount is then divided equally between the players.

<p>Source code <a href="https://github.com/wickens/ptree_library/tree/master/public_goods">here</a></p>
"""


class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'public_goods'


class Treatment(ptree.models.BaseTreatment):

    subsession = models.ForeignKey(Subsession)

    amount_allocated = models.MoneyField(
        null=True,
        doc="""Amount allocated to each participant"""
    )

    multiplication_factor = models.DecimalField(
        null=True,
        decimal_places=1,
        max_digits=2,
        doc="""The multiplication factor in group contribution"""
    )


class Match(ptree.models.BaseMatch):

    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    participants_per_match = 4

    contributions = models.MoneyField(
        null=True,
        doc="""Total amount contributed by the group players"""
    )

    individual_share = models.MoneyField(
        null=True,
        doc="""The amount each player in the group receives out of the the total contributed (after multiplication by some factor)"""
    )

    def set_contributions(self):
        """Sums up the amounts contributed to the joint project by each player in a group"""
        self.contributions = sum(p.contributed_amount for p in self.participants())

    def set_individual_share(self):
        """Calculates the amount each player in a group receives from the joint project"""
        self.individual_share = int((self.contributions * self.treatment.multiplication_factor) / self.participants_per_match)


class Participant(ptree.models.BaseParticipant):

    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)

    contributed_amount = models.MoneyField(
        null=True,
        doc="""The amount contributed by the player"""
    )

    def set_payoff(self):
        """Calculate participant payoff"""
        self.payoff = (self.treatment.amount_allocated - self.contributed_amount) + self.match.individual_share

    def contribute_choices(self):
        """Returns a list of allowed values for contribution"""
        return money_range(0, self.treatment.amount_allocated, 0.10)


def treatments():

    return [Treatment.create(amount_allocated=3.00, multiplication_factor=1.6)]
