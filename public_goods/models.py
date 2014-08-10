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

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    amount_allocated = models.MoneyField(
        default=3.00,
        doc="""Amount allocated to each participant"""
    )

    multiplication_factor = models.FloatField(
        default=1.6,
        doc="""The multiplication factor in group contribution"""
    )

    def contribute_choices(self):
        """Returns a list of allowed values for contribution"""
        return money_range(0, self.amount_allocated, 0.10)


class Match(ptree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    participants_per_match = 4

    contributions = models.MoneyField(
        default=None,
        doc="""Total amount contributed by the group players"""
    )

    individual_share = models.MoneyField(
        default=None,
        doc="""The amount each player in the group receives out of the the total contributed (after multiplication by some factor)"""
    )

    def set_contributions(self):
        """Sums up the amounts contributed to the joint project by each player in a group"""
        self.contributions = sum(p.contributed_amount for p in self.participants())

    def set_individual_share(self):
        """Calculates the amount each player in a group receives from the joint project"""
        self.individual_share = int((self.contributions * self.treatment.multiplication_factor) / self.participants_per_match)


class Participant(ptree.models.BaseParticipant):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    contributed_amount = models.MoneyField(
        default=None,
        doc="""The amount contributed by the player"""
    )

    def set_payoff(self):
        """Calculate participant payoff"""
        self.payoff = (self.treatment.amount_allocated - self.contributed_amount) + self.match.individual_share



def treatments():
    return [Treatment.create()]